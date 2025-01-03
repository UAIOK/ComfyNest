from firebase_config import db
from models import User
from firebase_admin import db as admin_db
from typing import Optional 

def get_user(db_reference, username: str) -> Optional[User]:  # Замінили на Optional[User]
    """
    Функція для отримання користувача з Firebase
    """
    ref = db_reference.reference(f'/users/{username}')  # Використовуємо передану змінну db_reference
    user_data = ref.get()
    if not user_data:
        return None
    return User(**user_data)

def create_user(db_reference, user: User):
    """
    Функція для додавання нового користувача в Firebase
    """
    ref = db_reference.reference(f'/users/{user.username}')
    ref.set(user.dict())  # зберігаємо дані у Firebase

def update_user(db_reference, username: str, user: User):
    """
    Функція для оновлення користувача в Firebase
    """
    ref = db_reference.reference(f'/users/{username}')
    ref.update(user.dict())  # оновлюємо дані користувача

def delete_user(db_reference, username: str):
    """
    Функція для видалення користувача з Firebase
    """
    ref = db_reference.reference(f'/users/{username}')
    ref.delete()  # видаляємо користувача
