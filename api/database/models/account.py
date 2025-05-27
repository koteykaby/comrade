from api.database.main import *
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.mutable import MutableDict, MutableList

class Account(base): 
    __tablename__ = "accounts"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    steamid = Column(Integer)
    data = Column(MutableDict.as_mutable(JSON)) 
    inventory = Column(MutableList.as_mutable(JSON))
    item_locations = Column(MutableList.as_mutable(JSON))