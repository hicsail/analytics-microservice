from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from .main import *
from .models import *
from .database import *

@app.get("/userScreenTime/{user_id}/{screen_id}", response_model=None)
def get_user_screen_time(user_id: str, screen_id: int) -> JSONResponse:
    try:
        # Get all sessions for the given user
        sessions = session.query(Session).filter(Session.userID == user_id).all()
        if not sessions:
            return JSONResponse(status_code=404, content={"message": "User not Found."})
        total_screen_time = 0
        for s in sessions:
            # Get all sessions with the given screen ID
            screens = session.query(Screen).filter(Screen.screenID == screen_id).all()
            for scr in screens:
                # Calculate total screen time
                if scr.startTime and scr.endTime:
                    total_screen_time += (scr.endTime - scr.startTime).total_seconds()

        # Return total screen time in seconds
        return JSONResponse(content={"user_id": user_id, "screen_id": screen_id, "screen_time(sec)": total_screen_time})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve screen time.')