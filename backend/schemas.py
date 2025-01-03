from pydantic import BaseModel, root_validator
from typing import Optional
import uuid

class UserInDB(BaseModel):
    id: str  # id обов'язкове після реєстрації
    username: str
    email: str
    hashed_password: str

    @root_validator(pre=True)
    def generate_id(cls, values):
        # Генерація id, якщо воно не передано
        if 'id' not in values:
            values['id'] = str(uuid.uuid4())
        return values

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str

    class Config:
        orm_mode = True

class UserCreate(User):
    password: str
