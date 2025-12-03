import json
import os
import sys

# Add parent directory to path to access shared config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import shared configuration
from config import DB_FILE, VOTING_FILE, ID_CARD_FOLDER

# Import local modules
try:
    from . import login, register, verification_voting, voting, logout
except ImportError:
    import login, register, verification_voting, voting, logout

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

# Add this function to user/main_user.py
def view_voting_sessions():
    """View available voting sessions"""
    from config import VOTING_SESSIONS_FILE
    import json
    
    sessions = load_json(VOTING_SESSIONS_FILE)
    
    print("\n" + "="*60)
    print("AVAILABLE VOTING SESSIONS")
    print("="*60)
    
    if not sessions:
        print("No voting sessions created yet.")
        print("Please wait for the admin to create a voting session.")
        return
    
    for session in sessions:
        status_emoji = {
            "active": "✅ VOTE NOW",
            "upcoming": "⏳ COMING SOON",
            "completed": "🏁 ENDED"
        }.get(session['status'], "❓ UNKNOWN")
        
        print(f"\n{session['id']}. {session['name']}")
        print(f"   Status: {status_emoji}")
        print(f"   Description: {session['description']}")
        print(f"   Period: {session['start_date']} {session['start_time']} to {session['end_date']} {session['end_time']}")
        
        if session['status'] == 'active':
            print(f"   👥 Candidates: {len(session['candidates'])}")
            print(f"   🗳️  Total Votes: {session['total_votes']}")
    
    print("="*60)
    input("\nPress Enter to continue...")

def user_dashboard(email):
    """User dashboard after login"""
    db = load_json(DB_FILE)
    
    while True:
        print("\n" + "="*50)
        print(f"USER DASHBOARD - Welcome {db[email]['username']}!")
        print("="*50)
        print("1. 🗳️  Voting Verification")
        print("2. 📋 View Voting Sessions")
        print("3. ✅ Cast Your Vote")
        print("4. 👤 View Profile")
        print("5. 🚪 Logout")
        print("="*50)

        choice = input("\nChoose option (1-5): ").strip()

        if choice == "1":
            verification_voting.voting_verification(email)
        elif choice == "2":
            view_voting_sessions()  # Add this function
        elif choice == "3":
            voting.vote(email)
        elif choice == "4":
            view_profile(email)
        elif choice == "5":
            logout.logout()
            break
        else:
            print("❌ Invalid option! Please enter 1-5.")

def display_user_welcome():
    """Display user welcome banner"""
    print("\n" + "="*50)
    print("         USER PORTAL")
    print("="*50)

def view_profile(email):
    """Display user profile information"""
    db = load_json(DB_FILE)
    voting_db = load_json(VOTING_FILE)
    
    print("\n" + "="*40)
    print("YOUR PROFILE")
    print("="*40)
    print(f"📧 Email: {email}")
    print(f"👤 Username: {db[email]['username']}")
    print(f"✅ Email Verified: {'Yes' if db[email]['verified'] else 'No'}")
    print(f"🗳️  Voting Verified: {'Yes' if db[email]['voting_verified'] else 'No'}")
    
    if email in voting_db:
        print("\n📋 Voting Information:")
        print(f"  👤 Full Name: {voting_db[email]['fullname']}")
        print(f"  ⚤ Gender: {voting_db[email]['gender']}")
        print(f"  📞 Phone: {voting_db[email]['phone']}")
        print(f"  🆔 ID Card: {os.path.basename(voting_db[email]['id_card'])}")
    
    if 'has_voted' in db[email] and db[email]['has_voted']:
        print(f"\n🗳️  Voting Status: Voted")
        print(f"   Candidate: {db[email].get('voted_for', 'N/A')}")
        print(f"   Time: {db[email].get('vote_time', 'N/A')}")
    else:
        print("\n🗳️  Voting Status: Not voted yet")
    print("="*40)

def user_dashboard(email):
    """User dashboard after login"""
    db = load_json(DB_FILE)
    
    while True:
        print("\n" + "="*50)
        print(f"USER DASHBOARD - Welcome {db[email]['username']}!")
        print("="*50)
        print("1. 🗳️  Voting Verification")
        print("2. ✅ Cast Your Vote")
        print("3. 👤 View Profile")
        print("4. 🚪 Logout")
        print("="*50)

        choice = input("\nChoose option (1-4): ").strip()

        if choice == "1":
            verification_voting.voting_verification(email)
        elif choice == "2":
            voting.vote(email)
        elif choice == "3":
            view_profile(email)
        elif choice == "4":
            logout.logout()
            break
        else:
            print("❌ Invalid option! Please enter 1-4.")

def main():
    """Main entry point for user portal"""
    display_user_welcome()
    
    while True:
        print("\n" + "="*40)
        print("USER MENU")
        print("="*40)
        print("1. 📝 Register New Account")
        print("2. 🔐 Login to Account")
        print("3. ↩️  Back to Main Portal")
        print("="*40)

        choice = input("\nChoose option (1-3): ").strip()

        if choice == "1":
            register.register()
        elif choice == "2":
            email = login.login()
            if email:
                user_dashboard(email)
        elif choice == "3":
            print("\nReturning to main portal...")
            break
        else:
            print("❌ Invalid option! Please enter 1-3.")

if __name__ == "__main__":
    main()