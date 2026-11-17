from app.db.database import SessionLocal
from app.models.department import Department


departments = [
    {
        "name": "Department of Civil Engineering",
        "code": "CE"
    },
    {
        "name": "Department of Computer Engineering",
        "code": "CO"
    },
    {
        "name": "Department of Electrical and Electronic Engineering",
        "code": "EE"
    },
    {
        "name": "Department of Mechanical Engineering",
        "code": "ME"
    },
    {
        "name": "Department of Interdisciplinary Studies",
        "code": "IS"
    }
]

def seed_departments():
    db = SessionLocal()

    try:
        for department_data in departments:
            existing_department = db.query(Department).filter(
                Department.code == department_data["code"]
            ).first()

            if existing_department:
                continue

            new_department = Department(
                name=department_data["name"],
                code=department_data["code"]
            )

            db.add(new_department)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

if __name__ == "__main__":
    seed_departments()
    print("Departments inserted successfully!")