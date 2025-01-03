from firebase_admin import db
import firebase_config  # Імпортуємо ініціалізацію Firebase

# Отримання посилання на корінь бази даних
ref = db.reference('/')

# Зчитування всіх даних з кореня
data = ref.get()

# Запис даних
ref.set({
    'child_data': {
        'name': 'Anna',
        'age': 19
    }
})

# Виведення отриманих даних
print(data)
