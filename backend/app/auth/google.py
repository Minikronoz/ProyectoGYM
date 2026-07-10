import requests
from typing import Optional, Dict, Any

from app.config import settings


def get_google_auth_url() -> str:
    if not settings.GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID not configured")

    from urllib.parse import urlencode
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


def get_google_token(code: str) -> Dict[str, Any]:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth credentials not configured")

    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI
        }
    )
    response.raise_for_status()
    return response.json()


def get_google_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    response.raise_for_status()
    return response.json()
