# voting_system/user/profile/view_profile.py
from database.db_connection import execute_query

def view_profile(email):
    """Display user profile information"""
    # Get user info with verification data
    query = """
    SELECT u.*, vv.fullname, vv.gender, vv.phone, vv.id_card_path
    FROM users u
    LEFT JOIN voting_verification vv ON u.email = vv.user_email
    WHERE u.email = %s
    """
    user = execute_query(query, (email,), fetch_one=True)
    
    if not user:
        print("❌ User not found!")
        input("Press Enter to continue...")
        return
    
    print("\n" + "="*50)
    print("👤 YOUR PROFILE")
    print("="*50)
    print(f"📧 Email: {email}")
    print(f"👤 Username: {user['username']}")
    print(f"✅ Email Verified: {'Yes' if user['email_verified'] else 'No'}")
    print(f"🗳  Voting Verified: {'Yes' if user['voting_verified'] else 'No'}")
    
    if user['fullname']:
        print(f"\n📋 Personal Information:")
        print(f"  👤 Full Name: {user['fullname']}")
        print(f"  ⚤ Gender: {user['gender'] or 'Not specified'}")
        print(f"  📞 Phone: {user['phone'] or 'Not provided'}")
    
    if user['has_voted']:
        print(f"\n🗳  Voting Status: ✅ Voted")
        print(f"   Candidate: {user.get('voted_for', 'N/A')}")
        print(f"   Session ID: {user.get('voted_session_id', 'N/A')}")
        print(f"   Time: {user.get('vote_time', 'N/A')}")
    else:
        print("\n🗳  Voting Status: ❌ Not voted yet")
    
    print("="*50)
    input("\nPress Enter to continue...")