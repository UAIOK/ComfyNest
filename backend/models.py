from pydantic import BaseModel

# Модель для створення користувача
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Модель для користувача в базі даних
class UserInDB(UserCreate):
    id: int
    hashed_password: str

# Модель для повернення користувача
class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True
