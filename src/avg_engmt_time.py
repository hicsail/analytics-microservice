from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from .main import *
from .models import *
from .database import *

# Calculate the average engagement time for a given user for the selected time period
@app.get("/averageEngagementTime/{user_id}/{time_period}", response_model=None)
def get_average_engagement(user_id: str, time_period: int) -> JSONResponse:
    try:
        # Get the sessions for the user
        sessions = session.query(Session).filter_by(userID=user_id).all()
    
        # Calculate the total engagement time for the user for the selected time period
        total_engagement_time = 0
        for s in sessions:
            if s.startTime and s.endTime:
                total_engagement_time += (s.endTime - s.startTime).total_seconds()

        # Calculate the average engagement time in seconds
        if total_engagement_time > 0:
            average_engagement_time = round(total_engagement_time / time_period)
            return JSONResponse(content={"user_id": user_id, "time_period": time_period, "average_engagement_time(sec)": average_engagement_time})
        else:
            return JSONResponse(content={"user_id": user_id, "time_period": time_period, "average_engagement_time(sec)": 0})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve average engagement time.')
