import getpass
import json
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import shared configuration
from config import DB_FILE

def load_json(path):
    """Helper function to load JSON data"""
    if not os.path.exists(path):
        return {}
    if os.path.getsize(path) == 0:
        return {}
    try:
        return json.load(open(path, "r"))
    except:
        return {}

def login():
    """Handle user login"""
    print("\n" + "="*40)
    print("USER LOGIN")
    print("="*40)
    
    gmail = input("Enter Gmail: ").strip().lower()
    
    db = load_json(DB_FILE)
    
    if gmail not in db:
        print("❌ Gmail not found.")
        return None

    password = getpass.getpass("Password: ")

    if db[gmail]["password"] != password:
        print("❌ Incorrect password.")
        return None

    if not db[gmail]["verified"]:
        print("❌ Your account is not verified!")
        return None

    print(f"\n✅ Welcome {db[gmail]['username']}!")
    return gmail