from pydantic import BaseModel, ConfigDict


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str


class MaintenanceTeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str