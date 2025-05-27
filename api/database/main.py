from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.mutable import MutableDict, MutableList

engine = create_engine('sqlite:///comrade.db', echo=True)

base = declarative_base()

class Account(base): 
    __tablename__ = "accounts"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    steamid = Column(Integer)
    data = Column(MutableDict.as_mutable(JSON)) 
    inventory = Column(MutableList.as_mutable(JSON))
    item_locations = Column(MutableList.as_mutable(JSON))
    
base.metadata.create_all(engine)

create_session = sessionmaker(bind=engine)
