from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ComplaintOption(Base):
    __tablename__ = "complaint_options"

    __table_args__ = (
        UniqueConstraint(
            "location_id",
            "name",
            name="uq_location_complaint_option"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    location_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False
    )

    complaint_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaint_categories.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )