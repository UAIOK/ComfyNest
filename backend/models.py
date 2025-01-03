from pydantic import BaseModel
from typing import Optional
import uuid

# Модель користувача, який створюється

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str
    password: str

    class Config:
        orm_mode = True


class UserInDB(UserCreate):
    id: str = str(uuid.uuid4())  # Генерація id за замовчуванням
    hashed_password: str

# Модель для повернення користувача
class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True
