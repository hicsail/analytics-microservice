from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timedelta
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING', '')

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
    occurTime = Column(DateTime)
    sessionID = Column(String(40))

class SessionTable(Base):
    __tablename__ = 'session'
    sessionID = Column(String(40), primary_key=True)
    userID = Column(String(40))
    startTime = Column(DateTime)
    endTime = Column(DateTime)

class Screen(Base):
    __tablename__ = 'screen'
    screenID = Column(Integer, primary_key=True)
    endTime = Column(DateTime)
    startTime = Column(DateTime)
    screenName = Column(String(50))
    sessionID = Column(String(40))


# Function to establish a connection to the MySQL database
def create_db_connection():
    try:
        engine = create_engine(DB_CONNECTION_STRING)
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

@app.get('/')
async def root():
    return {'message': 'The analytics service is running.'}

#write get api to select all user from sessiontable who have starttime in Month i choose
@app.get("/daily_active_users/{date}")
def get_daily_active_users(date: datetime) -> List[str]:
    #get users who have sessions with starttime on the given date
    try:
        result = session.query(SessionTable.userID).filter(SessionTable.startTime == date).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve daily active users.')

@app.get("/weekly_new_users/{date}")
def get_weekly_new_users(date: datetime) -> List[str]:
    #get user who have sessions with starttime within the last 14 days
    try:
        result = session.query(SessionTable.userID).filter(SessionTable.startTime >= date - timedelta(days=14)).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve weekly new users.')

@app.get("/monthly_active_users/{date}")
def get_monthly_active_users(date: datetime) -> List[str]:
    #get users who have sessions with starttime within the last 30 days
    try:
        result = session.query(SessionTable.userID).filter(SessionTable.startTime >= date - timedelta(days=60)).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve monthly active users.')
