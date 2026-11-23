from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import require_roles
from app.repositories.reference import (
    get_departments,
    get_active_maintenance_teams,
)
from app.schemas.reference import (
    DepartmentResponse,
    MaintenanceTeamResponse,
)


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin Reference Data"],
    dependencies=[Depends(require_roles("ADMIN"))],
)


@router.get(
    "/departments",
    response_model=list[DepartmentResponse],
)
def list_departments(db: Session = Depends(get_db)):
    return get_departments(db)


@router.get(
    "/maintenance-teams",
    response_model=list[MaintenanceTeamResponse],
)
def list_active_maintenance_teams(db: Session = Depends(get_db)):
    return get_active_maintenance_teams(db)