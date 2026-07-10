from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import (
    auth_router,
    gyms_router,
    exercises_router,
    workouts_router,
    sync_router,
    analytics_router
)

try:
    if settings.DATABASE_URL:
        Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    print("Server will run but database features will be unavailable.")

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(gyms_router)
app.include_router(exercises_router)
app.include_router(workouts_router)
app.include_router(sync_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "FlexLog API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
