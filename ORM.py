from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import MySQLdb

app = FastAPI()

# Create SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userID = Column(String(40))


class Event(Base):
    __tablename__ = 'event'
    eventID = Column(Integer, primary_key=True)
    eventName = Column(String(45))
    occurTime = Column(String(45))
    sessionID = Column(String(40))

class Session(Base):
    __tablename__ = 'session'
    sessionID = Column(String(40), primary_key=True)
    userID = Column(String(40))
    startTime = Column(String(45))
    endTime = Column(String(45))

class Screen(Base):
    __tablename__ = 'screen'
    screenID = Column(Integer, primary_key=True)
    endTime = Column(String(45))
    startTime = Column(String(45))
    screenName = Column(String(50))
    sessionID = Column(String(40))

# Function to establish a connection to the MySQL database
def create_db_connection():
    try:
        engine = create_engine('mysql://root:cMgpBzyj3m2KX9OD35s2@containers-us-west-145.railway.app:5515/dev')
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to connect to MySQL database.')

engine = create_db_connection()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# Insert a new user into the database
# new_user = User(userID='1234567890abcdef')
# session.add(new_user)
# session.commit()

# Insert a new event into the database
# new_Event = Event(eventID=7, eventName='test', occurTime=datetime.now(), sessionID='f3f9f478-e9d1-495b-8bfb-7fd11b70999f')
# session.add(new_Event)
# session.commit()