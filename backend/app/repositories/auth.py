
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    return user


def update_user_password(
    db: Session,
    user: User,
    password_hash: str
) -> User:

    user.password_hash = password_hash
    user.must_change_password = False

    db.flush()
    db.refresh(user)

    return user
