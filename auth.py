import json
import os
import hashlib
import re
from encryption import encrypt_data, decrypt_data

USERS_FILE    = "users.json"
DOCS_DIR      = "doctor_docs"
ADMIN_EMAIL   = "admin@nayana.com"
ADMIN_PASSWORD = hashlib.sha256("nayana@admin123".encode()).hexdigest()

# Accepts: MCI-12345 | KMC/12345/2020 | TNMC/A/12345 | 5-digit digits
LICENSE_PATTERN = re.compile(
    r'^([A-Z]{2,5}[-/][A-Z0-9/-]{2,20}|[0-9]{5,10})$',
    re.IGNORECASE
)

def validate_license(license_no):
    """Returns (True, '') or (False, reason)."""
    ln = license_no.strip()
    if not ln:
        return False, "License number is required."
    if ln in ("123", "000", "111", "999"):
        return False, "Please enter a valid license number."
    if not LICENSE_PATTERN.match(ln):
        return False, (
            "Invalid format. Use formats like MCI-12345, "
            "KMC/12345/2020, or your state council number."
        )
    return True, ""

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {"patients": {}, "doctors": {}}
    with open(USERS_FILE, 'rb') as f:
        raw = f.read()
    try:
        return json.loads(decrypt_data(raw))
    except:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)

def save_users(users):
    encrypted = encrypt_data(json.dumps(users, indent=2))
    with open(USERS_FILE, 'wb') as f:
        f.write(encrypted)

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
                    license_no, email, password, doc_path=""):
    # Layer 1 — license format check
    valid, reason = validate_license(license_no)
    if not valid:
        return False, reason

    users = load_users()
    if email in users["doctors"]:
        return False, "Email already registered"
    os.makedirs(DOCS_DIR, exist_ok=True)
    users["doctors"][email] = {
        "name":                name,
        "specialization":      specialization,
        "hospital":            hospital,
        "license_no":          license_no,
        "email":               email,
        "password":            hash_password(password),
        "verification_status": "pending",   # Layer 3 — starts pending
        "doc_path":            doc_path     # Layer 2 — uploaded doc
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
    # Layer 3 — block unverified doctors
    status = user.get("verification_status", "pending")
    if status == "pending":
        return False, None, "Your account is pending admin verification. You will be notified once approved."
    if status == "rejected":
        return False, None, "Your registration was rejected. Please contact support."
    return True, user, "Login successful"

def login_admin(email, password):
    if email == ADMIN_EMAIL and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD:
        return True, "Login successful"
    return False, "Invalid admin credentials"

def get_pending_doctors():
    users = load_users()
    return [u for u in users["doctors"].values()
            if u.get("verification_status") == "pending"]

def approve_doctor(email):
    users = load_users()
    if email in users["doctors"]:
        users["doctors"][email]["verification_status"] = "approved"
        save_users(users)

def reject_doctor(email):
    users = load_users()
    if email in users["doctors"]:
        users["doctors"][email]["verification_status"] = "rejected"
        save_users(users)
def get_all_doctors():
    users = load_users()
    return [u for u in users["doctors"].values()
            if u.get("verification_status") == "approved"]