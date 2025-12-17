# voting_system/user/auth/login.py
import getpass
import random
from database.db_connection import execute_query
from utils.email_service import send_otp_email

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT * FROM users WHERE email = %s"
    return execute_query(query, (email,), fetch_one=True)

def save_otp(email, otp_code, purpose):
    """Save OTP to database"""
    # Clean old OTPs first
    clean_query = "DELETE FROM otp_codes WHERE email = %s OR expires_at < NOW()"
    execute_query(clean_query, (email,))
    
    # Insert new OTP
    query = """
    INSERT INTO otp_codes (email, otp_code, purpose, expires_at)
    VALUES (%s, %s, %s, DATE_ADD(NOW(), INTERVAL 10 MINUTE))
    """
    return execute_query(query, (email, otp_code, purpose), lastrowid=True)

def verify_otp(email, otp_code):
    """Verify OTP from database"""
    query = """
    SELECT id FROM otp_codes 
    WHERE email = %s AND otp_code = %s AND expires_at > NOW()
    LIMIT 1
    """
    result = execute_query(query, (email, otp_code), fetch_one=True)
    
    if result:
        # Delete used OTP
        delete_query = "DELETE FROM otp_codes WHERE email = %s"
        execute_query(delete_query, (email,))
        return True
    
    return False

def login():
    """Handle user login with OTP verification"""
    print("\n" + "="*40)
    print("USER LOGIN")
    print("="*40)
    
    # Step 1: Get credentials
    email = input("Enter Email: ").strip().lower()
    
    user = get_user_by_email(email)
    
    if not user:
        print("❌ Email not found.")
        input("Press Enter to continue...")
        return None

    password = getpass.getpass("Password: ")

    if user["password"] != password:
        print("❌ Incorrect password.")
        input("Press Enter to continue...")
        return None

    if not user["email_verified"]:
        print("❌ Your account is not verified!")
        input("Press Enter to continue...")
        return None

    # Step 2: Generate and send OTP
    print("\n⏳ Generating OTP...")
    otp = str(random.randint(100000, 999999))
    
    # Save OTP to database
    save_otp(email, otp, "login")
    
    print("📧 Sending OTP to your email (check SPAM folder)...")
    if not send_otp_email(email, otp, "login"):
        print("❌ Failed to send OTP. Login cancelled.")
        input("Press Enter to continue...")
        return None

    # Step 3: Verify OTP
    print("\n" + "-"*40)
    print("OTP VERIFICATION")
    print("-"*40)
    user_otp = input("Enter the 6-digit OTP sent to your email: ").strip()

    if not verify_otp(email, user_otp):
        print("❌ Invalid or expired OTP!")
        input("Press Enter to continue...")
        return None

    print(f"\n✅ Welcome {user['username']}!")
    input("Press Enter to continue...")
    return email