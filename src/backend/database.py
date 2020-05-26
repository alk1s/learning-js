from sqlalchemy import create_engine, Column, Integer, Text, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import config

engine = create_engine(config.db_string, echo=True, convert_unicode=True)
db = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


class Click(Base):
    __tablename__ = 'clicks'
    _id = Column('id', Integer, primary_key=True)
    ip_address = Column(String(256), nullable=False)
    ip_useragent = Column(String(2048), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, _id, ip_address, ip_useragent):
        self._id = _id
        self.ip_address = ip_address
        self.ip_useragent = ip_useragent

    def __repr__(self):
        return '<Click %r>' % (self._id)


Base.metadata.create_all(bind=engine)
