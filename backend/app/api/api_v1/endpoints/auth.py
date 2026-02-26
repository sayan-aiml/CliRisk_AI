from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from app.core.config import settings
from app.services.auth_service import create_access_token, verify_password, get_password_hash
# In a real app, we would fetch the user from the DB
# For this MVP, we'll use a mock user check

router = APIRouter()

@router.post("/login/access-token")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Mock user for MVP
    print(f"DEBUG: Login attempt - username: {form_data.username}, password: {form_data.password}", flush=True)
    if form_data.username == "admin" and form_data.password == "admin123":
        user_id = "1"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/test-token")
def test_token() -> Any:
    """
    Test access token
    """
    return {"msg": "Token is valid"}
