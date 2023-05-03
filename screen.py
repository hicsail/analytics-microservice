from pydantic import BaseModel
from main import *
import traceback

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from session import is_valid_datetime, endTime_conflicts_startTime

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


screen_return_response_400 = {
    "missing_sessionID": {"status code":400, "message":"missing required field: sessionID"},
    "missing_screenName": {"status code":400, "message":"missing required field: screenName"},
    "missing_startTime": {"status code":400, "message":"missing required field: startTime"},
    "missing_screenID":{"status code":400, "message":"missing required field: screenID"},
    "missing_endTime":{"status code":400, "message":"missing required field: endTime"},
    "sessionID_not_match_screenID":{"status code":400, "message":"sessionID does not match screenID"},
    "screenName_not_match_screenID":{"status code":400, "message":"screenName does not match screenID"},   
    "screenID_not_exist":{"status code":400, "message":"screenID does not exists"},
    "session_not_exists":{"status code":400, "message":"sessionID does not exists"},
    "invalid_datetime": {"status code": 400,
                         "message": "provided datetime is either not in mysql datetime format nor an invalid datetime"},
    "endTime_already_exists":{"status code":400, "message":"screenID already had endTime"},
    "endTime_conflict_startTime": {"status code": 400, "message": "endTime conflicts with startTime"}
}

screen_return_response_200 = {
    "recorded_screen":{"status code":200, "message":"Set current screen successfully"},
    "set_screen_close_time":{"status code":200, "message":"Set screen endTime successfully"}
}


db_connection = create_db_connection()
Session = sessionmaker(bind=db_connection)
db_session = Session()


app = FastAPI()


@app.post("/api/analysis/update-current-screen-endTime/")
async def close_current_screen(item:CloseScreenItem):
    """
    Use it to set the close time of the screen. When a user closes a screen, the app can call this API to record the time
    that the user closes the screen
    :param item: CloseScreenItem. Hover and click it to see its data structure
    :return: 200, 400, or 500 HTTP Response
    """
    try:
        if item.sessionID is None or item.sessionID == "":
            return JSONResponse(status_code=400,content=screen_return_response_400["missing_sessionID"])
        if item.screenID is None or item.screenID == "":
            return JSONResponse(status_code=400,content=screen_return_response_400["missing_screenID"])
        if item.screenName is None or item.screenName == "":
            return JSONResponse(status_code=400,content=screen_return_response_400["missing_screenName"])
        if item.endTime is None or item.endTime == "":
            return JSONResponse(status_code=400, content=screen_return_response_400["missing_endTime"])
        if not is_valid_datetime(item.endTime):
            return JSONResponse(status_code=400, content=screen_return_response_400["invalid_datetime"])
        else:
            if not userSessionExists(item.sessionID):
                return JSONResponse(status_code=400,content=screen_return_response_400["session_not_exists"])
            row_check_result = checkCloseScreenRow(item)
            if row_check_result == "screenID not found":
                return JSONResponse(status_code=400, content=screen_return_response_400["screenID_not_exist"])
            if row_check_result == "endTime conflicts startTime":
                return JSONResponse(status_code=400, content=screen_return_response_400["endTime_conflict_startTime"])
            if row_check_result == "sessionID does not match screenID":
                return JSONResponse(status_code=400, content=screen_return_response_400["sessionID_not_match_screenID"])
            if row_check_result == "screenName does not match":
                return JSONResponse(status_code=400, content=screen_return_response_400["screenName_not_match_screenID"])
            if row_check_result == "endTime is not null":
                return JSONResponse(status_code=400, content=screen_return_response_400["endTime_already_exists"])
            else:
                updateScreenEndTime(item)
                return JSONResponse(status_code=200, content=screen_return_response_200["set_screen_close_time"])
    except Exception as e:
        traceback.print_exc()
        db_session.rollback()
        raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})


def updateScreenEndTime(item: CloseScreenItem):
    """
    Use it to update the endTime of a screen whose screenID matches the one provided in the CloseScreenItem
    :param item: CloseScreenItem. Hover and click it to see its data structure
    """
    row = db_session.query(ScreenTable).filter_by(screenID=item.screenID).first()
    row.endTime = item.endTime
    db_session.commit()


def checkCloseScreenRow(item: CloseScreenItem):
    """
    Given a CloseScreenItem item, use this to checks if the given Item matches a row in the screen table. If there is
    anything unmatched, it will return a message, so the function that calls this function will return 400 response
    :param item: CloseScreenItem. Hover and click it to see its data structure
    :return: string that represent the checking result
    """
    result = db_session.query(ScreenTable).filter_by(screenID=item.screenID).first()
    if result is None:
        return "screenID not found"
    if result.sessionID != item.sessionID:
        return "sessionID does not match screenID"
    if result.screenName != item.screenName:
        return "screenName does not match"
    if endTime_conflicts_startTime(result.startTime,item.endTime):
        return "endTime conflicts startTime"
    if result.endTime is not None:
        return "endTime is not null"


@app.post("/api/analysis/setCurrentScreen/")
async def set_current_screen(item:RecordScreenItem):
    """
    Use it to add a screen into the screen database. The screen has the information contained in the RecordScreenItem
    item.
    :param item: The RecordScreenItem. Hover and click it to see its data structure
    :return: 200, 400, or 500 HTTPResponse
    """
    try:
        if item.sessionID is None or item.sessionID == "":
            return JSONResponse(status_code=400,content=screen_return_response_400["missing_sessionID"])
        if item.screenName is None or item.screenName == "":
            return JSONResponse(status_code=400,content=screen_return_response_400["missing_screenName"])
        if item.startTime is None or item.startTime == "":
            return JSONResponse(status_code=400,content=screen_return_response_400["missing_startTime"])
        if not is_valid_datetime(item.startTime):
            return JSONResponse(status_code=400,content=screen_return_response_400["invalid_datetime"])
        else:
            if not userSessionExists(item.sessionID):
                return JSONResponse(status_code=400,content=screen_return_response_400["session_not_exists"])
            else:
                recorded_screen = ScreenTable(sessionID=item.sessionID,screenName=item.screenName, startTime=item.startTime)
                db_session.add(recorded_screen)
                db_session.flush()
                db_session.commit()
                db_session.refresh(recorded_screen)
                data = screen_return_response_200["recorded_screen"]
                data["screenID"] = recorded_screen.screenID
                return JSONResponse(status_code=200, content=data)
    except Exception as e:
        traceback.print_exc()
        db_session.rollback()
        raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})


def userSessionExists(targetSessionID):
    """
    Use this function to check if a session that has the targetSessionID exists in the database
    :param targetSessionID:
    :return: True if there is session that has the targetSessionID, False if there is not.
    """
    result = db_session.query(SessionTable).filter(SessionTable.sessionID==targetSessionID)
    return len(result.all())==1 

