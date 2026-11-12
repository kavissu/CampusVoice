
from app.models.location import Location
from app.models.hall import Hall
from app.models.department import Department
from app.models.equipment_type import EquipmentType
from app.models.equipment import Equipment

from app.repositories.public import (
    get_hall_equipment_by_qr_token
)


def create_repository_test_data(db):
    department = Department(
        name="Computer Engineering",
        code="CO"
    )

    equipment_type = EquipmentType(
        name="Computer Equipment"
    )

    location = Location(
        name="Repository Test Hall",
        code="REPO-TEST-001",
        location_type="LECTURE_HALL",
        qr_code_token="repository-test-token",
        is_active=True
    )

    db.add_all([department, equipment_type, location])
    db.flush()

    hall = Hall(
        name="Repository Test Hall",
        code="REPO-HALL-001",
        location_id=location.id,
        is_active=True
    )

    db.add(hall)
    db.flush()

    active_equipment = Equipment(
        name="Test Computer",
        asset_code="REPO-PC-001",
        equipment_type_id=equipment_type.id,
        department_id=department.id,
        hall_id=hall.id,
        is_active=True
    )

    inactive_equipment = Equipment(
        name="Inactive Projector",
        asset_code="REPO-PROJ-001",
        equipment_type_id=equipment_type.id,
        department_id=department.id,
        hall_id=hall.id,
        is_active=False
    )

    db.add_all([active_equipment, inactive_equipment])
    db.commit()

    return location


def test_repository_returns_active_hall_equipment(db_session):
    location = create_repository_test_data(db_session)

    result = get_hall_equipment_by_qr_token(
        db_session,
        location.qr_code_token
    )

    assert result is not None

    returned_location, hall, equipment_list = result

    assert returned_location.name == "Repository Test Hall"
    assert hall.name == "Repository Test Hall"
    assert len(equipment_list) == 1
    assert equipment_list[0].name == "Test Computer"


def test_repository_returns_none_for_invalid_token(db_session):
    create_repository_test_data(db_session)

    result = get_hall_equipment_by_qr_token(
        db_session,
        "invalid-repository-token"
    )

    assert result is None


def test_repository_returns_none_for_inactive_location(db_session):
    location = create_repository_test_data(db_session)

    location.is_active = False
    db_session.commit()

    result = get_hall_equipment_by_qr_token(
        db_session,
        location.qr_code_token
    )

    assert result is None


def test_repository_returns_none_for_inactive_hall(db_session):
    location = create_repository_test_data(db_session)

    hall = (
        db_session.query(Hall)
        .filter(Hall.location_id == location.id)
        .first()
    )

    hall.is_active = False
    db_session.commit()

    result = get_hall_equipment_by_qr_token(
        db_session,
        location.qr_code_token
    )

    assert result is None
