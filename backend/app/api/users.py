
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.database import get_db
from app.dependencies.auth import require_roles
from app.models.user import User
from app.schemas.user import UserCreateRequest, UserCreateResponse
from app.services.user import create_user_account


router = APIRouter()


@router.post(
    "/",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN"))
):
    try:
        result = create_user_account(
            db=db,
            full_name=request.full_name,
            email=str(request.email),
            role_name=request.role,
            department_id=request.department_id,
            maintenance_team_id=request.maintenance_team_id,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User could not be created because the data conflicts with an existing record"
        )
