from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UsersModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    first_name: str
    last_name: str
    phone: str
    is_active: bool
    email_verified: bool
    phone_verified: bool
    created_at: datetime
    updated_at: datetime
    password_changed_at: datetime

class UsersRequestModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    password: str


class UsersUpdateModel(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UserActivityModel(BaseModel):
    is_active: bool
