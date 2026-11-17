
from app.models.location import Location
from app.models.hall import Hall
from app.models.department import Department
from app.models.equipment_type import EquipmentType
from app.models.equipment import Equipment

from app.services.public import get_public_hall_equipment


def create_service_test_data(db):
    department = Department(
        name="Computer Engineering",
        code="CO"
    )

    equipment_type = EquipmentType(
        name="Computer Equipment"
    )

    location = Location(
        name="Service Test Hall",
        code="SERVICE-TEST-001",
        location_type="LECTURE_HALL",
        qr_code_token="service-test-token",
        is_active=True
    )

    db.add_all([department, equipment_type, location])
    db.flush()

    hall = Hall(
        name="Service Test Hall",
        code="SERVICE-HALL-001",
        location_id=location.id,
        is_active=True
    )

    db.add(hall)
    db.flush()

    equipment = Equipment(
        name="Service Test Computer",
        asset_code="SERVICE-PC-001",
        equipment_type_id=equipment_type.id,
        department_id=department.id,
        hall_id=hall.id,
        is_active=True
    )

    db.add(equipment)
    db.commit()

    return location


def test_service_returns_hall_equipment(db_session):
    location = create_service_test_data(db_session)

    result = get_public_hall_equipment(
        db_session,
        location.qr_code_token
    )

    assert result is not None
    assert result["location"]["name"] == "Service Test Hall"
    assert result["hall"]["name"] == "Service Test Hall"
    assert result["total_equipment"] == 1
    assert len(result["equipment"]) == 1
    assert result["equipment"][0]["name"] == "Service Test Computer"


def test_service_returns_none_for_invalid_token(db_session):
    create_service_test_data(db_session)

    result = get_public_hall_equipment(
        db_session,
        "invalid-service-token"
    )

    assert result is None
