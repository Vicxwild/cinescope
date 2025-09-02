from pydantic import BaseModel, Field, field_validator, ConfigDict, field_serializer
from constants.roles import Roles
from typing import Optional
import datetime
from uuid import UUID

class TestUser(BaseModel):
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

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

class LoginUserResponse(BaseModel):
    id: UUID
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: list[Roles]
