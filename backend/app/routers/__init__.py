from app.routers.auth import router as auth_router
from app.routers.gyms import router as gyms_router
from app.routers.exercises import router as exercises_router
from app.routers.workouts import router as workouts_router
from app.routers.sync import router as sync_router
from app.routers.analytics import router as analytics_router

__all__ = [
    "auth_router",
    "gyms_router",
    "exercises_router",
    "workouts_router",
    "sync_router",
    "analytics_router"
]
