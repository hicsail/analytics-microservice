from fastapi import FastAPI
from .routers.users import router as user_router
from .routers.sessions import router as session_router
from .routers.screen import router as screen_router
from .routers.event import router as event_router
from .routers.screen_time import router as screen_time_router
from .routers.avg_engmt_time import router as avg_engmt_time_router

app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="Core API",
    description="Analytical Microservice",
    version="1.0",
    openapi_url="/api/v2/openapi.json",
)
app.include_router(user_router)
app.include_router(session_router)
app.include_router(screen_router)
app.include_router(event_router)
app.include_router(screen_time_router)
app.include_router(avg_engmt_time_router)

@app.get('/')
async def root():
    return {'message': 'The analytics service is running.'}
