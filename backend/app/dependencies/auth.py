
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.role import Role
from app.core.security import verify_access_token


# HTTP Bearer authentication
oauth2_scheme = HTTPBearer(auto_error=False)


# Get the currently authenticated user
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Check whether the token is provided
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials are required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        # Verify JWT token
        payload = verify_access_token(credentials.credentials)

        # Extract user ID from token
        user_id = int(payload.get("sub"))

    except (InvalidTokenError, TypeError, ValueError):
        raise credentials_exception

    # Find user in database
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    # Check whether user exists and is active
    if user is None or not user.is_active:
        raise credentials_exception

    return user


# Prevent users from accessing normal APIs
# before changing their temporary password
def get_current_user_without_password_change(
    current_user: User = Depends(get_current_user)
) -> User:

    if current_user.must_change_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must change your password before accessing this resource"
        )

    return current_user


# Allow authenticated users to access password change API
def get_user_allowed_to_change_password(
    current_user: User = Depends(get_current_user)
) -> User:

    return current_user


# Check user role before allowing access
def require_roles(*allowed_roles: str):

    def role_checker(
        current_user: User = Depends(
            get_current_user_without_password_change
        ),
        db: Session = Depends(get_db)
    ) -> User:

        # Get user's role from database
        role = (
            db.query(Role)
            .filter(Role.id == current_user.role_id)
            .first()
        )

        # Verify role permission
        if role is None or role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker
