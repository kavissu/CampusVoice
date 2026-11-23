from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.maintenance_team import MaintenanceTeam


def get_departments(db: Session):
    return (
        db.query(Department)
        .order_by(Department.name.asc(), Department.id.asc())
        .all()
    )


def get_active_maintenance_teams(db: Session):
    return (
        db.query(MaintenanceTeam)
        .filter(MaintenanceTeam.is_active.is_(True))
        .order_by(MaintenanceTeam.name.asc(), MaintenanceTeam.id.asc())
        .all()
    )