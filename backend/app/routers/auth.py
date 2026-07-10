from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.auth import create_access_token, verify_password, get_password_hash, get_google_auth_url, get_google_token, get_google_user_info
from app.auth.jwt import verify_token
from app.config import settings
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(
        email=user_data.email,
        name=user_data.name,
        google_id=user_data.google_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.google_id or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/google/url")
def google_auth_url():
    try:
        url = get_google_auth_url()
        return {"url": url}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    try:
        token_data = get_google_token(code)
        access_token = token_data.get("access_token")
        user_info = get_google_user_info(access_token)

        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("id")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email, name=name, google_id=google_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        elif not user.google_id:
            user.google_id = google_id
            if not user.name:
                user.name = name
            db.commit()

        jwt_token = create_access_token(data={"sub": user.id})
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google auth failed: {str(e)}")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
