from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RecordEventItem(BaseModel):
    sessionID: str
    eventName: str
    occurTime: str



class Event(Base):
    __tablename__ = 'event'
    eventID = Column(INT, primary_key=true)
    sessionID = Column(VARCHAR, ForeignKey('session.sessionID'))
    eventName = Column(VARCHAR)
    occurTime = Column(VARCHAR)

class session(Base):
    __tablename__ = 'session'
    sessionID = Column(VARCHAR, primary_key=true)
    userID = Column(VARCHAR, ForeignKey('user.userID'))
    startTime = Column(VARCHAR, nullable=False)
    endTime = Column(VARCHAR, nullable=True)

return_response_400 = {
    "missing_sessionID": {"status code":400, "message":"missing required field: sessionID"},
    "missing_eventName": {"status code":400, "message":"missing required field: eventName"},
    "missing_occurTime": {"status code":400, "message":"missing required field: occurTime"},
    "session_not_exists":{"status code":400, "message":"SessionID does not exists"}
}

return_response_200 = {
    "recorded_event":{"status code":200, "message":"Record event successfully"}
}


app = FastAPI()

@app.post("/api/analysis/record-event/")
async def record_event(item:RecordEventItem):
    # try:
    if item.sessionID == None or item.sessionID == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_sessionID"])
    if item.eventName == None or item.eventName == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_eventName"])
    if item.occurTime == None or item.occurTime == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_occurTime"])
    else:
        if not userSessionExists(item.sessionID):
            return JSONResponse(status_code=400,content=return_response_400["session_not_exists"])
        else:
            recorded_event = Event(sessionID=item.sessionID,eventName=item.eventName, occurTime=item.occurTime)
            db_session=getSession()
            db_session.add(recorded_event)
            db_session.commit()
            return JSONResponse(status_code=200, content=return_response_200["recorded_event"])
    # except Exception as e:
    #     print("Here")
    #     print(e)
        # raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})


def getEngine():
    return create_engine("mysql+pymysql://root:cMgpBzyj3m2KX9OD35s2@containers-us-west-145.railway.app:5515/dev")


def getSession():
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def userSessionExists(targetSessionID):
    db_session = getSession()
    result = db_session.query(session).filter(session.sessionID==targetSessionID)
    return len(result.all())==1 

