
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    ChangePasswordRequest,
    PasswordChangeResponse
)
from app.services.auth import (
    authenticate_user,
    change_user_password
)
from app.models.user import User
from app.dependencies.auth import get_user_allowed_to_change_password


router = APIRouter(tags=["Authentication"])


# User Login
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    result = authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    return result


# Change Password
@router.post(
    "/change-password",
    response_model=PasswordChangeResponse
)
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_user_allowed_to_change_password
    )
):
    result = change_user_password(
        db=db,
        user=current_user,
        current_password=password_data.current_password,
        new_password=password_data.new_password
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password or new password must be different"
        )

    return result
