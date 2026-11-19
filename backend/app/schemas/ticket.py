
from typing import Literal

from pydantic import BaseModel, Field, model_validator,ConfigDict
from datetime import datetime

class EquipmentFaultCreate(BaseModel):
    equipment_id: int

    problem_option_id: int | None = None

    problem_description: str | None = Field(
        default=None,
        max_length=1000
    )

    urgency_reason: Literal[
        "Class in progress",
        "Can be resolved later"
    ]

    @model_validator(mode="after")
    def validate_problem_details(self):
        if self.problem_option_id is None and not self.problem_description:
            raise ValueError(
                "Select a problem option or provide a description"
            )

        if self.problem_description is not None:
            self.problem_description = self.problem_description.strip()

        if self.problem_description == "":
            self.problem_description = None

        if self.problem_option_id is None and self.problem_description is None:
            raise ValueError(
                "Select a problem option or provide a description"
            )

        return self

class EquipmentFaultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tracking_code: str
    ticket_type: str
    problem_description: str
    priority: str
    status: str
    reported_at: datetime
