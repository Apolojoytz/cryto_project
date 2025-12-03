import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import from config
from config import load_json, save_json, DB_FILE, VOTING_FILE, VOTING_SESSIONS_FILE

# Import admin modules
try:
    import login
    import create_voting
    import result
    import blockchain_viewer
    import logout
except ImportError:
    from . import login, create_voting, result, blockchain_viewer, logout

def display_admin_welcome():
    """Display admin welcome banner"""
    print("\n" + "="*50)
    print("         ADMIN CONTROL PANEL")
    print("="*50)

def view_all_users():
    """View all registered users"""
    db = load_json(DB_FILE)
    voting_db = load_json(VOTING_FILE)
    
    print("\n" + "="*70)
    print("ALL REGISTERED USERS")
    print("="*70)
    print(f"{'No.':<4} {'Email':<30} {'Username':<20} {'Voting Verified':<15} {'Has Voted':<10}")
    print("-" * 70)
    
    for i, (email, data) in enumerate(db.items(), 1):
        voting_status = "✅ Yes" if data.get('voting_verified', False) else "❌ No"
        voted_status = "✅ Yes" if data.get('has_voted', False) else "❌ No"
        print(f"{i:<4} {email:<30} {data['username']:<20} {voting_status:<15} {voted_status:<10}")
    
    print(f"\n📊 Statistics:")
    print(f"  Total Users: {len(db)}")
    print(f"  Voting Verified: {sum(1 for u in db.values() if u.get('voting_verified', False))}")
    print(f"  Voted: {sum(1 for u in db.values() if u.get('has_voted', False))}")
    print("="*70)
    
    input("\nPress Enter to continue...")

def delete_user():
    """Delete a user account"""
    db = load_json(DB_FILE)
    voting_db = load_json(VOTING_FILE)
    
    print("\n" + "="*50)
    print("DELETE USER ACCOUNT")
    print("="*50)
    
    # Show users first
    print("Current Users:")
    for email, data in db.items():
        print(f"  {email} - {data['username']}")
    
    email = input("\nEnter user email to delete: ").strip().lower()
    
    if email not in db:
        print("❌ User not found!")
        return
    
    confirm = input(f"⚠️  Are you sure you want to delete {email}? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        # Remove from users database
        username = db[email]['username']
        del db[email]
        
        # Remove from voting database if exists
        if email in voting_db:
            del voting_db[email]
        
        # Save changes
        save_json(DB_FILE, db)
        save_json(VOTING_FILE, voting_db)
        
        print(f"✅ User '{username}' ({email}) has been deleted.")
        
        # Record deletion on blockchain
        try:
            from config import get_blockchain
            blockchain = get_blockchain()
            
            deletion_data = {
                "email": email,
                "username": username,
                "action": "user_deletion",
                "timestamp": "deleted"
            }
            
            blockchain.add_transaction("user_deletion", deletion_data)
            print("   📗 Deletion recorded on blockchain")
        except:
            print("   ⚠️  Could not record deletion on blockchain")
    else:
        print("❌ Deletion cancelled.")

def reset_voting():
    """Reset voting data (clear all votes)"""
    db = load_json(DB_FILE)
    sessions = load_json(VOTING_SESSIONS_FILE)
    
    print("\n" + "="*50)
    print("RESET VOTING DATA")
    print("="*50)
    print("⚠️  WARNING: This will clear ALL voting records!")
    print("   - All users' 'has_voted' status will be reset")
    print("   - All vote records will be cleared")
    print("   - User accounts will NOT be deleted")
    
    confirm = input("\nAre you sure? Type 'RESET' to confirm: ").strip()
    
    if confirm == "RESET":
        # Reset voting status for all users
        reset_count = 0
        for email in db:
            if db[email].get('has_voted', False):
                db[email]['has_voted'] = False
                if 'voted_for' in db[email]:
                    del db[email]['voted_for']
                if 'vote_time' in db[email]:
                    del db[email]['vote_time']
                if 'voted_session_id' in db[email]:
                    del db[email]['voted_session_id']
                if 'vote_id' in db[email]:
                    del db[email]['vote_id']
                reset_count += 1
        
        # Reset session votes
        session_reset_count = 0
        for session in sessions:
            if session['total_votes'] > 0:
                session['total_votes'] = 0
                session['voters'] = []
                for candidate in session['candidates']:
                    candidate['votes'] = 0
                session_reset_count += 1
        
        # Save changes
        save_json(DB_FILE, db)
        save_json(VOTING_SESSIONS_FILE, sessions)
        
        # Record reset on blockchain
        try:
            from config import get_blockchain
            blockchain = get_blockchain()
            
            reset_data = {
                "action": "voting_reset",
                "users_reset": reset_count,
                "sessions_reset": session_reset_count,
                "timestamp": "reset"
            }
            
            blockchain.add_transaction("system", reset_data)
            print(f"✅ All voting data has been reset! (Recorded on blockchain)")
            print(f"   Users reset: {reset_count}")
            print(f"   Sessions reset: {session_reset_count}")
        except:
            print(f"✅ All voting data has been reset!")
            print(f"   Users reset: {reset_count}")
            print(f"   Sessions reset: {session_reset_count}")
    else:
        print("❌ Reset cancelled.")

def admin_dashboard():
    """Admin dashboard after login"""
    while True:
        print("\n" + "="*50)
        print("ADMIN DASHBOARD")
        print("="*50)
        print("1. 👥 View All Users")
        print("2. 🗑️  Delete User Account")
        print("3. 🗳️  Create Voting Session")
        print("4. 📋 View Voting Sessions")
        print("5. 📊 View Voting Results")
        print("6. 📗 View Blockchain")
        print("7. 🔄 Reset Voting Data")
        print("8. 🚪 Logout")
        print("="*50)

        choice = input("\nChoose option (1-8): ").strip()

        if choice == "1":
            view_all_users()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            create_voting.create_voting_session()
        elif choice == "4":
            create_voting.view_voting_sessions()
        elif choice == "5":
            result.view_results()
        elif choice == "6":
            blockchain_viewer.view_blockchain()
        elif choice == "7":
            reset_voting()
        elif choice == "8":
            logout.admin_logout()
            break
        else:
            print("❌ Invalid option! Please enter 1-8.")

def main():
    """Main entry point for admin panel"""
    display_admin_welcome()
    
    # Admin login
    if not login.admin_login():
        print("❌ Admin login failed. Exiting...")
        return
    
    # Show admin dashboard
    admin_dashboard()

if __name__ == "__main__":
    main()