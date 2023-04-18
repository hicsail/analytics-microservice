from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RecordScreenItem(BaseModel):
    sessionID: str
    screenName: str
    startTime: str


class CloseScreenItem(BaseModel):
    screenID: int
    sessionID: str
    screenName: str
    endTime: str


class Screen(Base):
    __tablename__ = 'screen'
    screenID = Column(INT, primary_key=true)
    sessionID = Column(VARCHAR, ForeignKey('session.sessionID'))
    screenName = Column(VARCHAR)
    startTime = Column(VARCHAR)
    endTime = Column(VARCHAR, nullable=True)

class session(Base):
    __tablename__ = 'session'
    sessionID = Column(VARCHAR, primary_key=true)
    userID = Column(VARCHAR, ForeignKey('user.userID'))
    startTime = Column(VARCHAR, nullable=False)
    endTime = Column(VARCHAR, nullable=True)

screen_return_response_400 = {
    "missing_sessionID": {"status code":400, "message":"missing required field: sessionID"},
    "missing_screenName": {"status code":400, "message":"missing required field: screenName"},
    "missing_startTime": {"status code":400, "message":"missing required field: startTime"},
    "missing_screenID":{"status code":400, "message":"missing required field: screenID"},
    "missing_endTime":{"status code":400, "message":"missing required field: endTime"},
    "sessionID_not_match_screenID":{"status code":400, "message":"sessisonID does not match screenID"},
    "screenName_not_match_screenID":{"status code":400, "message":"screenName does not match screenID"},   
    "screenID_not_exist":{"status code":400, "message":"screenID does not exists"},
    "session_not_exists":{"status code":400, "message":"sessionID does not exists"},
    "endTime_already_exists":{"status code":400, "message":"screenID already had endTime"}
}

screen_return_response_200 = {
    "recorded_screen":{"status code":200, "message":"Set current screen successfully"},
    "set_screen_close_time":{"status code":200, "message":"Set screen endTime successfully"}
}


app = FastAPI()

@app.post("/api/analysis/closeCurrentScreen/")
async def close_current_screen(item:CloseScreenItem):
    # try:
    if item.sessionID == None or item.sessionID == "":
        return JSONResponse(status_code=400,content=screen_return_response_400["missing_sessionID"])
    if item.screenID == None or item.screenID == "":
        return JSONResponse(status_code=400,content=screen_return_response_400["missing_screenID"])
    if item.screenName == None or item.screenName == "":
        return JSONResponse(status_code=400,content=screen_return_response_400["missing_screenName"])
    if item.endTime == None or item.endTime == "":
        return JSONResponse(status_code=400, content=screen_return_response_400["missing_endTime"])
    else:
        if not userSessionExists(item.sessionID):
            return JSONResponse(status_code=400,content=screen_return_response_400["session_not_exists"])
        row_check_result = checkCloseScreenRow(item)
        if row_check_result == "screenID not found":
            return JSONResponse(status_code=400, content=screen_return_response_400["screenID_not_exist"])
        if row_check_result == "sessionID does not match screenID":
            return JSONResponse(status_code=400, content=screen_return_response_400["sessionID_not_match_screenID"])
        if row_check_result == "screenName does not match":
            return JSONResponse(status_code=400, content=screen_return_response_400["screenName_not_match_screenID"])
        if row_check_result == "endTime is not null":
            return JSONResponse(status_code=400, content=screen_return_response_400["endTime_already_exists"])
        else:
            updateScreenEndTime(item)
            return JSONResponse(status_code=200, content=screen_return_response_200["set_screen_close_time"])
    # except Exception as e:
    #     print("Here")
    #     print(e)
        # raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})

def updateScreenEndTime(item: CloseScreenItem):
    db_session = getSession()
    row = db_session.query(Screen).filter_by(screenID=item.screenID).first()
    row.endTime = item.endTime
    db_session.commit()

def checkCloseScreenRow(item: CloseScreenItem):
    db_session = getSession()
    result = db_session.query(Screen).filter_by(screenID=item.screenID).first()
    if result is None:
        return "screenID not found"
    if result.sessionID != item.sessionID:
        return "sessionID does not match screenID"
    if result.screenName != item.screenName:
        return "screenName does not match"
    if result.endTime != None:
        return "endTime is not null"


@app.post("/api/analysis/setCurrentScreen/")
async def set_current_screen(item:RecordScreenItem):
    # try:
    if item.sessionID == None or item.sessionID == "":
        return JSONResponse(status_code=400,content=screen_return_response_400["missing_sessionID"])
    if item.screenName == None or item.screenName == "":
        return JSONResponse(status_code=400,content=screen_return_response_400["missing_screenName"])
    if item.startTime == None or item.startTime == "":
        return JSONResponse(status_code=400,content=screen_return_response_400["missing_startTime"])
    else:
        if not userSessionExists(item.sessionID):
            return JSONResponse(status_code=400,content=screen_return_response_400["session_not_exists"])
        else:
            recorded_screen = Screen(sessionID=item.sessionID,screenName=item.screenName, startTime=item.startTime)
            db_session=getSession()
            db_session.add(recorded_screen)
            db_session.commit()
            return JSONResponse(status_code=200, content=screen_return_response_200["recorded_screen"])
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

