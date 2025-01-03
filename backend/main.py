from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from firebase_config import db  # Імпортуємо Firebase DB
from models import UserCreate, UserInDB, User
from crud import create_user, get_user  # Імпортуємо функції для роботи з Firebase
from auth import create_access_token, authenticate_user, get_current_user, get_current_active_user, get_current_admin, get_password_hash  # Імпортуємо функції аутентифікації
from fastapi.security import OAuth2PasswordRequestForm  # Імпортуємо форму для аутентифікації
from datetime import timedelta

# Конфігурація для роботи з FastAPI та Firebase
app = FastAPI()

# Реєстрація нового користувача
@app.post("/register")
async def register_user(user: UserCreate):
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)  # Хешуємо пароль
    new_user = UserInDB(**user.dict(), hashed_password=hashed_password)

    create_user(db, new_user)  # Додаємо користувача до Firebase
    return {"message": "User registered successfully"}

# Аутентифікація користувача та отримання токену
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Отримання даних користувача
@app.get("/users/{username}")
async def read_user(username: str):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Отримання даних про елементи
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int | None = None):
    ref = db.reference(f'/items/{item_id}')
    item_data = ref.get()
    if item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item = {
        "item_id": item_id,
        "needy": needy,
        "skip": skip,
        "limit": limit,
        "item_data": item_data
    }
    return item

# Приватні маршрути для авторизованих користувачів
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

# Адміністративний маршрут
@app.get("/admin/")
async def admin_route(current_admin: User = Depends(get_current_admin)):
    return {"message": f"Hello, {current_admin.username}. You have admin access."}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the ComfyNest API!"}

