# voting_system/user/voting/verification.py
import os
import shutil
from database.db_connection import execute_query
from config import ID_CARD_FOLDER

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT voting_verified FROM users WHERE email = %s"
    return execute_query(query, (email,), fetch_one=True)

def save_voting_verification(email, fullname, gender, phone, id_card_path):
    """Save voting verification data"""
    query = """
    INSERT INTO voting_verification (user_email, fullname, gender, phone, id_card_path)
    VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(query, (email, fullname, gender, phone, id_card_path), lastrowid=True)

def update_user_voting_status(email):
    """Update user's voting verification status"""
    query = "UPDATE users SET voting_verified = TRUE WHERE email = %s"
    return execute_query(query, (email,))

def voting_verification(email):
    """Handle voting verification process"""
    print("\n" + "="*40)
    print("VOTING VERIFICATION")
    print("="*40)
    
    user = get_user_by_email(email)
    if not user:
        print("❌ User not found!")
        input("Press Enter to continue...")
        return False
    
    # Check if already verified
    if user["voting_verified"]:
        print("✅ You are already verified for voting!")
        input("Press Enter to continue...")
        return True

    # Get user information
    fullname = input("Full Name: ").strip()
    if not fullname:
        print("❌ Full name cannot be empty.")
        input("Press Enter to continue...")
        return False
    
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
        input("Press Enter to continue...")
        return False
    
    # Validate file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    ext = os.path.splitext(image_path)[1]
    
    if ext not in valid_extensions:
        print("❌ Invalid file type. Please use jpg, jpeg, or png.")
        input("Press Enter to continue...")
        return False

    # Copy ID card to database folder
    save_filename = f"{email}_{os.path.basename(image_path)}"
    save_path = os.path.join(ID_CARD_FOLDER, save_filename)
    
    try:
        shutil.copy(image_path, save_path)
        print(f"✅ ID card saved as: {save_filename}")
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        input("Press Enter to continue...")
        return False

    # Save voting verification data
    verification_id = save_voting_verification(email, fullname, gender, phone, save_path)
    
    if not verification_id:
        print("❌ Failed to save verification data.")
        input("Press Enter to continue...")
        return False

    # Update user verification status
    update_user_voting_status(email)

    print("\n" + "="*40)
    print("✅ Voting verification completed successfully!")
    print("You can now participate in voting.")
    print("="*40)
    
    input("Press Enter to continue...")
    return True