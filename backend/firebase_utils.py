import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from dotenv import load_dotenv

load_dotenv()
cred_path = os.getenv("FIREBASE_CRED_PATH")
cred = credentials.Certificate(cred_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def sign_up(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return {"email": email, "uid": user.uid}
    except:
        return None

def sign_in(email, password):
    users = db.collection("users").where("email", "==", email).get()
    for user in users:
        user_data = user.to_dict()
        if user_data.get("password") == password:
            return user_data
    return None


def update_list(email, list_type, movie):
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if list_type not in data:
            data[list_type] = []
        if movie not in data[list_type]:
            data[list_type].append(movie)
        doc_ref.set(data)
    else:
        doc_ref.set({"email": email, list_type: [movie]})

def get_user_lists(email):
    doc = db.collection("users").document(email).get()
    return doc.to_dict() if doc.exists else {}


