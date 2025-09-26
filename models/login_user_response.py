from pydantic import BaseModel, Field
from constants.roles import Roles
from uuid import UUID

class LoginUserResponse(BaseModel):
    id: UUID
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: list[Roles]
