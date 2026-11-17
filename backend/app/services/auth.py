
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.auth import (
    get_user_by_email,
    update_user_password
)

from app.core.security import (
    verify_password,
    create_access_token,
    hash_password
)


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> dict | None:

    # Find user using email
    user = get_user_by_email(db, email)

    # Reject if user does not exist
    if user is None:
        return None

    # Reject if password is incorrect
    if not verify_password(password, user.password_hash):
        return None

    # Reject inactive accounts
    if not user.is_active:
        return None

    # Generate JWT using the actual database user ID
    access_token = create_access_token(
        user_id=user.id,
        must_change_password=user.must_change_password
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



def change_user_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str
) -> dict | None:

    # Verify the current password
    if not verify_password(current_password, user.password_hash):
        return None

    # Prevent reusing the same password
    if verify_password(new_password, user.password_hash):
        return None

    # Hash the new password
    new_hashed_password = hash_password(new_password)

    # Update the database
    try:
        updated_user = update_user_password(
            db=db,
            user=user,
            password_hash=new_hashed_password
        )

        db.commit()
        db.refresh(updated_user)

    except Exception:
        db.rollback()
        raise

    # Create a normal access token
    access_token = create_access_token(
        user_id=updated_user.id,
        must_change_password=False
    )

    return {
        "message": "Password changed successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }
