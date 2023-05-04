from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__ = 'user'
    userID = Column(String(40), primary_key=True)

class Event(Base):
    __tablename__ = 'event'
    eventID = Column(Integer, primary_key=True)
    eventName = Column(String(45))
    occurTime = Column(DateTime)
    sessionID = Column(String(40))

class Session(Base):
    __tablename__ = 'session'
    sessionID = Column(String(40), primary_key=True)
    userID = Column(String(40))
    startTime = Column(DateTime)
    endTime = Column(DateTime, nullable=True)

class Screen(Base):
    __tablename__ = 'screen'
    screenID = Column(Integer, primary_key=True)
    endTime = Column(DateTime, nullable=True)
    startTime = Column(DateTime)
    screenName = Column(String(50))
    sessionID = Column(String(40))
