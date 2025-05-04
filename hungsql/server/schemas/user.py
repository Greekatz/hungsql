from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    
    class Config:
        extra = "forbid"  # Prevent extra fields
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "john_doe"
            }
        }

class UserCreate(UserBase):
    first_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                **UserBase.Config.json_schema_extra["example"],
                "first_name": "John",
                "password": "SecurePass123"
            }
        }
    
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
    @field_validator('password')
    # Validate password, input params: class, value
    def validate_password(cls, v):
        if v is not None:
            return UserCreate.validate_password(v)
        return v

class UserOut(UserBase):
    id: int
    first_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attribute = True


class UserInDB(UserBase):
    hashed_password: str

