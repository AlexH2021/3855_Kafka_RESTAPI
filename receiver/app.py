from datetime import datetime
import logging.config, connexion, requests, yaml, uuid, json
from sqlalchemy import true
import app_conf as cfg
from pykafka import KafkaClient

# read log config yml
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def post_acc(body):
    trace_id = str(uuid.uuid4())
    body['traceID'] = trace_id
    body['createdAt'] = str(datetime.now().replace(microsecond=0))

    print(body)
    kafka_hosts = f"{cfg.events['hostname']}:{cfg.events['port']}"
    client = KafkaClient(hosts=kafka_hosts)
    topic = client.topics[str.encode(cfg.events['topic'])]
    producer = topic.get_sync_producer()
    msg = { 
        "type": "requests_post_acc",
        "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": body 
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    #request received log
    logger.info(f'Received event sent Account data request with a trace id of {trace_id}')

    return msg

def post_trade(body):
    trace_id = str(uuid.uuid4())
    body['traceID'] = trace_id
    body['createdAt'] = str(datetime.now().replace(microsecond=0))
   
    kafka_hosts = f"{cfg.events['hostname']}:{cfg.events['port']}"
    client = KafkaClient(hosts=kafka_hosts)
    topic = client.topics[str.encode(cfg.events['topic'])]
    producer = topic.get_sync_producer()
    msg = { 
        "type": "requests_post_trade",
        "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payload": body 
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    #request received log
    logger.info(f'Received event Account request with a trace id of {trace_id}')

    return msg

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('receiver_api.yaml',strict_validation=True,validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080, debug=True)