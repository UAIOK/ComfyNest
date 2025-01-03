import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("C:/Users/Anna/LP/project/ComfyNest/backend/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://comfynest-ir-default-rtdb.europe-west1.firebasedatabase.app/'  # Ваша URL Firebase Database
})

ref = db.reference('/')