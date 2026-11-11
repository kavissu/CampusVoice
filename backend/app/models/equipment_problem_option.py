from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EquipmentProblemOption(Base):
    __tablename__ = "equipment_problem_options"

    __table_args__ = (
        UniqueConstraint(
            "equipment_type_id",
            "problem_name",
            name="uq_equipment_type_problem"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    equipment_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("equipment_types.id"),
        nullable=False
    )

    problem_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    fault_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fault_categories.id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )