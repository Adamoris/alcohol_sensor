import pyrebase
import json

config_path = 'firebaseConfiguration.json'

with open(config_path) as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

def write_to_firebase(data):
    db.child("users").child(f"{auth.current_user['localId']}").update(data)

def read_from_firebase():
    return db.child("users").child(f"{auth.current_user['localId']}").child("alcohol_detected").get().val()

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        return None
    
def register(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except:
        return None
    
def send_email_verification(user):
    auth.send_email_verification(user['idToken'])