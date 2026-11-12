
from pydantic import BaseModel


class PublicLocationResponse(BaseModel):
    id: int
    name: str
    code: str


class PublicHallResponse(BaseModel):
    id: int
    name: str
    code: str


class PublicEquipmentResponse(BaseModel):
    id: int
    name: str
    asset_code: str
    description: str | None = None


class PublicHallEquipmentResponse(BaseModel):
    location: PublicLocationResponse
    hall: PublicHallResponse
    equipment: list[PublicEquipmentResponse]
    total_equipment: int
