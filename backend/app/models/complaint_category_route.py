from sqlalchemy import (
    ForeignKey,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ComplaintCategoryRoute(Base):
    __tablename__ = "complaint_category_routes"

    __table_args__ = (
        UniqueConstraint(
            "complaint_category_id",
            "department_id",
            name="uq_complaint_category_department"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    complaint_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaint_categories.id"),
        nullable=False
    )

    department_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    maintenance_team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("maintenance_teams.id"),
        nullable=False
    )