# voting_system/debug_otp.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import execute_query

def debug_otp_system():
    """Debug OTP system"""
    print("🔧 DEBUGGING OTP SYSTEM")
    print("="*60)
    
    # 1. Check if table exists
    check_table = """
    SELECT COUNT(*) as table_exists 
    FROM information_schema.tables 
    WHERE table_schema = 'voting_system_db' 
    AND table_name = 'otp_codes'
    """
    result = execute_query(check_table, fetch_one=True)
    
    if result and result['table_exists']:
        print("✅ OTP table exists")
    else:
        print("❌ OTP table doesn't exist!")
        print("   Run setup.py again to create table")
        return
    
    # 2. Check table structure
    print("\n📋 Table structure:")
    describe = "DESCRIBE otp_codes"
    columns = execute_query(describe, fetch=True)
    
    if columns:
        for col in columns:
            print(f"   {col['Field']}: {col['Type']}")
    else:
        print("   Could not get table structure")
    
    # 3. Check for data
    print("\n📊 OTP data:")
    count_query = "SELECT COUNT(*) as total FROM otp_codes"
    count = execute_query(count_query, fetch_one=True)
    print(f"   Total OTPs: {count['total'] if count else 0}")
    
    recent_query = """
    SELECT * FROM otp_codes 
    ORDER BY created_at DESC 
    LIMIT 5
    """
    recent = execute_query(recent_query, fetch=True)
    
    if recent:
        print("   Recent OTPs:")
        for otp in recent:
            print(f"   - {otp['email']}: {otp['otp_code']} ({otp['purpose']})")
            print(f"     Expires: {otp['expires_at']}")
    else:
        print("   No OTPs found")
    
    # 4. Clean old OTPs
    print("\n🧹 Cleaning expired OTPs...")
    clean_query = "DELETE FROM otp_codes WHERE expires_at < NOW()"
    cleaned = execute_query(clean_query)
    print(f"   Deleted {cleaned if cleaned else 0} expired OTPs")
    
    # 5. Test OTP functions
    print("\n🧪 Testing OTP functions...")
    test_email = "test@example.com"
    test_otp = "999999"
    
    # Save OTP
    save_query = """
    INSERT INTO otp_codes (email, otp_code, purpose, expires_at)
    VALUES (%s, %s, 'test', DATE_ADD(NOW(), INTERVAL 10 MINUTE))
    """
    save_result = execute_query(save_query, (test_email, test_otp), lastrowid=True)
    
    if save_result:
        print(f"   ✅ Saved test OTP: {test_otp} for {test_email}")
        
        # Verify OTP
        verify_query = """
        SELECT id FROM otp_codes 
        WHERE email = %s AND otp_code = %s AND expires_at > NOW()
        LIMIT 1
        """
        verify_result = execute_query(verify_query, (test_email, test_otp), fetch_one=True)
        
        if verify_result:
            print(f"   ✅ OTP verification works")
            
            # Clean up test
            delete_query = "DELETE FROM otp_codes WHERE email = %s"
            execute_query(delete_query, (test_email,))
            print(f"   ✅ Cleaned up test data")
        else:
            print(f"   ❌ OTP verification failed")
    else:
        print(f"   ❌ Failed to save test OTP")
    
    print("="*60)
    print("📝 RECOMMENDATIONS:")
    
    # Check the actual problem
    if count and count['total'] == 0:
        print("1. OTP table exists but empty")
        print("2. Check if save_otp() function is being called")
        print("3. Check email_service.py is working")
    elif recent:
        print("1. OTPs are being saved")
        print("2. Check if verify_otp() function is working")
        print("3. Check OTP expiry time")
    else:
        print("1. Run setup.py to ensure table exists")
        print("2. Check database connection")
    
    print("="*60)
    input("Press Enter to continue...")

if __name__ == "__main__":
    debug_otp_system()