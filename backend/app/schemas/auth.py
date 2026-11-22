from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)

class PasswordChangeResponse(BaseModel):
    message: str
    access_token: str
    token_type: str


class CurrentUserResponse(BaseModel):
    id: int
    name: str
    role: str
    is_active: bool
    must_change_password: bool