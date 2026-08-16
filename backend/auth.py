import json
import os
import bcrypt

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def signup(username, password, profile):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {
        "password": hashed,
        "profile": profile
    }
    save_users(users)
    return True, "Account created"

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"
    if bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        return True, "Login successful"
    return False, "Incorrect password"

def get_profile(username):
    users = load_users()
    return users.get(username, {}).get("profile", {})

def update_profile(username, profile):
    users = load_users()
    if username in users:
        users[username]["profile"] = profile
        save_users(users)
        return True
    return False