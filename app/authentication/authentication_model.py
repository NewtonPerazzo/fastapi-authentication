from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LoginRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str

class UserCredentialsModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    password_hash: str
    is_active: bool
    password_changed_at: datetime

class UserSessionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    refresh_token_hash: str
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime
    last_used_at: datetime | None

class UserSessionCreateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    refresh_token_hash: str
    expires_at: datetime

class TokenResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_token_expires_in: int

class RefreshTokenRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str

class AccessTokenPayloadModel(BaseModel):
    sub: str
    sid: str
    type: str
    jti: str
    iat: int
    exp: int
    iss: str
    aud: str

class ResetPasswordBodyModel(BaseModel):
    refresh_token: str
    new_password: str
