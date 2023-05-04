from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .main import *
from .models import *
from .database import *

# Get the screen name for a given screen ID
def get_screen_name(screen_id: int):
    screen = session.query(Screen).filter_by(screenID=screen_id).first()
    if screen:
        return screen.screenName
    else:
        return JSONResponse(content={"message": "Screen not found."})

# Calculate the total screen time for a given screen ID
def get_total_screen_time(screen_id: int):
    screens = session.query(Screen).filter_by(screenID=screen_id).all()
    total_screen_time = 0
    for scr in screens:
        if scr.startTime and scr.endTime:
            total_screen_time += (scr.endTime - scr.startTime).total_seconds()
    return total_screen_time

# Get the average screen time per session for a given screen ID
def get_average_screen_time_per_session(screen_id: int):
    screens = session.query(Screen).filter_by(screenID=screen_id).all()
    total_session_count = len(screens)
    total_screen_time = get_total_screen_time(screen_id)
    if total_session_count > 0:
        average_screen_time_per_session = total_screen_time / total_session_count
        return average_screen_time_per_session
    else:
        return 0

# Get screen statistics for a given screen ID
@app.get("/screenTimeStatistics/{screen_id}", response_model=None)
def get_screen_time_statistics(screen_id: int) -> JSONResponse:
    try:
        screen_name = get_screen_name(screen_id)
        total_screen_time = get_total_screen_time(screen_id)
        average_screen_time_per_session = get_average_screen_time_per_session(screen_id)
        return JSONResponse(content={
            "screen_id": screen_id,
            "screen_name": screen_name,
            "total_screen_time(sec)": total_screen_time,
            "average_screen_time_per_session(sec)": average_screen_time_per_session
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve screen time statistics.')
