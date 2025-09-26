from pydantic import BaseModel, Field, field_validator, field_serializer
from constants.roles import Roles
from typing import Optional
from uuid import UUID

class TestUserModel(BaseModel):
    id: Optional[UUID] = None
    email: str = Field(...)
    fullName: str
    password: str = Field(..., min_length=8)
    passwordRepeat: str = Field(..., min_length=8, description='Repeat password')
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Password must match with password repeat")
        return v

    @field_serializer("roles", when_used="json")
    def serialize_roles(self, value: list[Roles]) -> list[str]:
        return [roles.value for roles in value]
