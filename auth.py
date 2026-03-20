import json
import os
import hashlib

USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {"patients": {}, "doctors": {}}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_patient(name, age, gender, email, password):
    users = load_users()
    if email in users["patients"]:
        return False, "Email already registered"
    users["patients"][email] = {
        "name":     name,
        "age":      age,
        "gender":   gender,
        "email":    email,
        "password": hash_password(password)
    }
    save_users(users)
    return True, "Registered successfully"

def register_doctor(name, specialization, hospital,
                    license_no, email, password):
    users = load_users()
    if email in users["doctors"]:
        return False, "Email already registered"
    users["doctors"][email] = {
        "name":           name,
        "specialization": specialization,
        "hospital":       hospital,
        "license_no":     license_no,
        "email":          email,
        "password":       hash_password(password)
    }
    save_users(users)
    return True, "Registered successfully"

def login_patient(email, password):
    users = load_users()
    if email not in users["patients"]:
        return False, None, "Email not found"
    user = users["patients"][email]
    if user["password"] != hash_password(password):
        return False, None, "Incorrect password"
    return True, user, "Login successful"

def login_doctor(email, password):
    users = load_users()
    if email not in users["doctors"]:
        return False, None, "Email not found"
    user = users["doctors"][email]
    if user["password"] != hash_password(password):
        return False, None, "Incorrect password"
    return True, user, "Login successful"