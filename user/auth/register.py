# voting_system/user/auth/register.py
import getpass
import random
from database.db_connection import execute_query
from utils.email_service import send_otp_email

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT id FROM users WHERE email = %s"
    return execute_query(query, (email,), fetch_one=True)

def create_user(email, username, password):
    """Create new user"""
    query = """
    INSERT INTO users (email, username, password, email_verified)
    VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (email, username, password, True), lastrowid=True)

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

def register():
    """Handle new user registration"""
    print("\n" + "="*40)
    print("REGISTRATION")
    print("="*40)
    
    email = input("Enter Email: ").strip().lower()
    
    # Basic email validation
    if "@" not in email or "." not in email:
        print("❌ Please enter a valid email address.")
        input("Press Enter to continue...")
        return None
    
    # Check if email already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        print("❌ This email is already registered.")
        input("Press Enter to continue...")
        return None

    username = input("Username: ").strip()
    
    if not username:
        print("❌ Username cannot be empty.")
        input("Press Enter to continue...")
        return None
    
    password = getpass.getpass("Password: ")
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters long.")
        input("Press Enter to continue...")
        return None
    
    confirm = getpass.getpass("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match!")
        input("Press Enter to continue...")
        return None

    # Generate and send OTP
    print("\n⏳ Generating OTP...")
    otp = str(random.randint(100000, 999999))
    
    # Save OTP to database
    save_otp(email, otp, "registration")
    
    print("📧 Sending OTP to your email (check SPAM folder)...")
    if not send_otp_email(email, otp, "registration"):
        print("❌ Failed to send OTP. Registration cancelled.")
        input("Press Enter to continue...")
        return None

    # Verify OTP
    print("\n" + "-"*40)
    print("OTP VERIFICATION")
    print("-"*40)
    user_otp = input("Enter the 6-digit OTP sent to your email: ").strip()

    if not verify_otp(email, user_otp):
        print("❌ Invalid or expired OTP! Registration failed.")
        input("Press Enter to continue...")
        return None

    # Create user in database
    result = create_user(email, username, password)
    
    if result:
        print("\n✅ Registration successful! You can now login.")
        input("Press Enter to continue...")
        return email
    else:
        print("❌ Registration failed. Please try again.")
        input("Press Enter to continue...")
        return None