import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..schemas import RecordEventItem
from ..models import Event, Session
from utils.utils import is_valid_datetime
from ..database import create_db_session

"""
File description:
This is the file that contains the POST endpoints related to event
"""

db_session = create_db_session()


return_response_400 = {
    "missing_sessionID": {"status code":400, "message":"missing required field: sessionID"},
    "missing_eventName": {"status code":400, "message":"missing required field: eventName"},
    "missing_occurTime": {"status code":400, "message":"missing required field: occurTime"},
    "session_not_exists":{"status code":400, "message":"SessionID does not exists"},
    "invalid_datetime": {"status code": 400, "message": "provided datetime is either not in mysql datetime format nor an invalid datetime"}
}

return_response_200 = {
    "recorded_event":{"status code":200, "message":"Record event successfully"}
}


router = APIRouter()


@router.post("/event/record")
async def record_event(item:RecordEventItem):
    """
    Use it to store an event into the database
    :param item: RecordEventItem. Hover and click it to see its data structure
    :return: 200, 400, or 500 HTTPResponse
    """
    try:
        if item.sessionID is None or item.sessionID == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_sessionID"])
        if item.eventName is None or item.eventName == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_eventName"])
        if item.occurTime is None or item.occurTime == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_occurTime"])
        if not is_valid_datetime(item.occurTime):
            return JSONResponse(status_code=400,content=return_response_400["invalid_datetime"])
        else:
            if not userSessionExists(item.sessionID):
                return JSONResponse(status_code=400,content=return_response_400["session_not_exists"])
            else:
                recorded_event = Event(sessionID=item.sessionID,eventName=item.eventName, occurTime=item.occurTime)
                db_session.add(recorded_event)
                db_session.flush()
                db_session.commit()
                db_session.refresh(recorded_event)
                data = return_response_200["recorded_event"]
                data["eventID"] = recorded_event.eventID
                return JSONResponse(status_code=200, content=data)
    except Exception as e:
        traceback.print_exc()
        db_session.rollback()
        raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})



def userSessionExists(targetSessionID):
    """
    Use it to check if there is a session whose sessionID exists in the Session table
    :param targetSessionID:
    :return: True if there is a session whose sessionID exists in the Session table, otherwise return False.
    """
    result = db_session.query(Session).filter(Session.sessionID==targetSessionID)
    return len(result.all())==1

