from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List
from models import *
from database import session


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'The analytics service is running.'}

@app.get("/daily_active_users/{date}")
def get_daily_active_users(date: datetime) -> List[str]:
    '''
    get users who have sessions with start time on the given date
    '''
    try:
        result = session.query(Session.userID).filter(Session.startTime == date).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve daily active users.')

@app.get("/weekly_new_users/{date}")
def get_weekly_new_users(date: datetime) -> List[str]:
    '''
    get user who have sessions with start time within the last 14 days
    '''
    try:
        result = session.query(Session.userID).filter(Session.startTime >= date - timedelta(days=14)).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve weekly new users.')

@app.get("/monthly_active_users/{date}")
def get_monthly_active_users(date: datetime) -> List[str]:
    '''
    get users who have sessions with start time within the last 30 days
    '''
    try:
        result = session.query(Session.userID).filter(Session.startTime >= date - timedelta(days=60)).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve monthly active users.')
