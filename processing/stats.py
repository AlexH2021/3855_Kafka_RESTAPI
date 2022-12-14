from sqlalchemy import Column, Integer, DateTime
from base import Base


class Stats(Base):
    """ Account """
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_account = Column(Integer)
    num_trade = Column(Integer)
    total_cash = Column(Integer)
    total_value = Column(Integer)
    total_share = Column(Integer)
    created_at = Column(DateTime)

    def __init__(self, num_account, num_trade, total_cash, total_value, total_share, created_at):
        """ Initializes an account """
        self.num_account = num_account
        self.num_trade = num_trade
        self.total_cash = total_cash
        self.total_value = total_value
        self.total_share = total_share
        self.created_at = created_at

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}