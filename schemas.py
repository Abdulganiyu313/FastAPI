from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    is_staff: Optional[bool]
    is_active: Optional[bool]
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john_doe@example.com",
                "password": "password",
                "full_name": "John Doe",
                "is_staff": False,
                "is_active": True
            }
        }


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_staff: bool
    is_active: bool

    
class OrderCreate(BaseModel):
    quantity: int = Field(..., gt=0)
    pizza_size: str = Field(..., pattern="^(SMALL|MEDIUM|LARGE|EXTRA_LARGE)$")
    user_id: int

class OrderRead(BaseModel):
    id: int
    quantity: int
    pizza_size: str
    user_id: int

    class Config:
        from_attributes = True
        
class Settings(BaseModel):
    authjwt_secret_key: str = '0e75f25ce65651bfba2dfff997d490cf26ff033134d3626cf4139ef52c921bb5'
    
class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "password"
            }
        }