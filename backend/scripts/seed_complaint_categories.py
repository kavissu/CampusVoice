
from app.db.database import SessionLocal
from app.models.complaint_category import ComplaintCategory


def seed_complaint_categories():
    db = SessionLocal()

    categories = [
        "Cleaning",
        "Electrical",
        "Water / Sanitation",
        "Canteen",
        "Infrastructure",
        "Security",
        "Other"
    ]

    try:
        for category_name in categories:

            existing_category = (
                db.query(ComplaintCategory)
                .filter(ComplaintCategory.name == category_name)
                .first()
            )

            if existing_category is None:
                new_category = ComplaintCategory(
                    name=category_name
                )

                db.add(new_category)

        db.commit()

        print("Complaint categories seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_complaint_categories()
