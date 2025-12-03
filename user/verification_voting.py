import json
import os
import shutil
import hashlib
from datetime import datetime
from config import DB_FILE, VOTING_FILE, ID_CARD_FOLDER, get_blockchain, save_json, load_json

def voting_verification(email):
    """Handle voting verification process with blockchain"""
    print("\n" + "="*40)
    print("VOTING VERIFICATION")
    print("="*40)
    
    db = load_json(DB_FILE)
    voting_db = load_json(VOTING_FILE)
    blockchain = get_blockchain()
    
    # Check if already verified
    if db[email]["voting_verified"]:
        print("✅ You are already verified for voting!")
        return True

    # Get user information
    fullname = input("Full Name: ").strip()
    
    # Gender input with validation
    gender = ""
    while gender.lower() not in ["male", "female", "other"]:
        gender = input("Gender (Male/Female/Other): ").strip().capitalize()
        if gender.lower() not in ["male", "female", "other"]:
            print("❌ Please enter Male, Female, or Other")

    phone = input("Phone Number: ").strip()
    
    # Validate phone number
    if not phone.isdigit() or len(phone) < 10:
        print("⚠️  Please enter a valid phone number")
        phone = input("Phone Number: ").strip()

    image_path = input("Path to ID Card Image (jpg/png/jpeg): ").strip()

    if not os.path.exists(image_path):
        print("❌ Image not found! Please check the path.")
        return False
    
    # Validate file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    ext = os.path.splitext(image_path)[1]
    
    if ext not in valid_extensions:
        print("❌ Invalid file type. Please use jpg, jpeg, or png.")
        return False

    # Copy ID card to database folder
    save_filename = f"{email}_idcard{ext}"
    save_path = os.path.join(ID_CARD_FOLDER, save_filename)
    
    try:
        shutil.copy(image_path, save_path)
        print(f"✅ ID card saved as: {save_filename}")
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return False

    # Calculate ID card hash for blockchain
    try:
        with open(save_path, 'rb') as f:
            id_card_hash = hashlib.sha256(f.read()).hexdigest()[:16]
    except:
        id_card_hash = "error"

    # Save voting data to regular database
    voting_db[email] = {
        "fullname": fullname,
        "gender": gender,
        "phone": phone,
        "id_card": save_path,
        "id_card_hash": id_card_hash,
        "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Update user verification status
    db[email]["voting_verified"] = True

    # Save data to regular database
    save_json(VOTING_FILE, voting_db)
    save_json(DB_FILE, db)
    
    # Record verification on blockchain
    verification_data = {
        "email": email,
        "fullname": fullname,
        "id_card_hash": id_card_hash,
        "action": "voting_verification",
        "timestamp": datetime.now().isoformat()
    }
    
    blockchain.add_transaction("verification", verification_data)

    print("\n" + "="*40)
    print("✅ Voting verification completed successfully!")
    print("   📗 Transaction recorded on blockchain")
    print("   🗳️  You can now participate in voting.")
    print("="*40)
    
    return True