
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreateRequest(BaseModel):

    full_name: str = Field(min_length=2, max_length=150)

    email: EmailStr

    role: Literal["LECTURER", "TECHNICIAN"]

    department_id: int = Field(gt=0)

    maintenance_team_id: int | None = Field(
        default=None,
        gt=0
    )


class UserCreateResponse(BaseModel):

    id: int
    full_name: str
    email: EmailStr
    role: Literal["LECTURER", "TECHNICIAN"]
    temporary_password: str
    must_change_password: bool
