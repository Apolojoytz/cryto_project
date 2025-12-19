# voting_system/admin/users/view_users.py
from database.db_connection import execute_query

def get_all_users():
    """Get all users with their verification status"""
    query = """
    SELECT u.*, vv.fullname, vv.gender, vv.phone,
           COUNT(v.id) as total_votes
    FROM users u
    LEFT JOIN voting_verification vv ON u.email = vv.user_email
    LEFT JOIN votes v ON u.email = v.user_email
    GROUP BY u.id, u.email, u.username, u.password, u.email_verified, 
             u.voting_verified, u.has_voted, u.voted_for, u.vote_time, 
             u.voted_session_id, u.created_at,
             vv.fullname, vv.gender, vv.phone
    ORDER BY u.created_at DESC
    """
    return execute_query(query, fetch=True)

def view_all_users():
    """View all registered users"""
    users = get_all_users()
    
    print("\n" + "="*60)
    print("👥 ALL REGISTERED USERS")
    print("="*60)
    
    if not users:
        print("No users registered yet.")
        input("\nPress Enter to continue...")
        return
    
    total_users = len(users)
    verified_users = sum(1 for user in users if user['email_verified'])
    voting_verified = sum(1 for user in users if user['voting_verified'])
    voted_users = sum(1 for user in users if user['has_voted'])
    
    print(f"📊 Statistics:")
    print(f"  • Total Users: {total_users}")
    print(f"  • Email Verified: {verified_users}")
    print(f"  • Voting Verified: {voting_verified}")
    print(f"  • Voted Users: {voted_users}")
    print("="*60)
    
    # Display user details
    for i, user in enumerate(users, 1):
        print(f"\n{i}. 📧 {user['email']}")
        print(f"   👤 Username: {user['username']}")
        print(f"   ✅ Email Verified: {'Yes' if user['email_verified'] else 'No'}")
        print(f"   🗳  Voting Verified: {'Yes' if user['voting_verified'] else 'No'}")
        print(f"   📝 Has Voted: {'Yes' if user['has_voted'] else 'No'}")
        print(f"   🗳  Total Votes: {user['total_votes']}")
        
        if user['fullname']:
            print(f"   📋 Full Name: {user['fullname']}")
            print(f"   ⚤ Gender: {user['gender'] or 'Not specified'}")
            print(f"   📞 Phone: {user['phone'] or 'Not provided'}")
        
        if user['has_voted']:
            print(f"   🗳  Voted For: {user.get('voted_for', 'N/A')}")
            print(f"   ⏰ Vote Time: {user.get('vote_time', 'N/A')}")
    
    print("="*60)
    input("\nPress Enter to continue...")