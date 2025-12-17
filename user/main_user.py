# voting_system/user/main_user.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import execute_query
from user.auth.login import login
from user.auth.register import register
from user.voting.verification import voting_verification
from user.voting.voting import vote
from user.profile.view_profile import view_profile
from user.profile.logout import logout

def display_user_welcome():
    """Display user welcome banner"""
    print("\n" + "="*50)
    print("         USER PORTAL - VOTING SYSTEM")
    print("="*50)

def get_user_info(email):
    """Get user information from database"""
    query = "SELECT username FROM users WHERE email = %s"
    user = execute_query(query, (email,), fetch_one=True)
    return user

def user_dashboard(email):
    """User dashboard after login"""
    user = get_user_info(email)
    if not user:
        print("❌ User not found!")
        return
    
    while True:
        print("\n" + "="*50)
        print(f"USER DASHBOARD - Welcome {user['username']}!")
        print("="*50)
        print("1. 🗳  Voting Verification")
        print("2. ✅ Cast Your Vote")
        print("3. 👤 View Profile")
        print("4. 🚪 Logout")
        print("="*50)

        choice = input("\nChoose option (1-4): ").strip()

        if choice == "1":
            voting_verification(email)
        elif choice == "2":
            vote(email)
        elif choice == "3":
            view_profile(email)
        elif choice == "4":
            logout()
            break
        else:
            print("❌ Invalid option! Please enter 1-4.")
            input("Press Enter to continue...")

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
            register()
        elif choice == "2":
            email = login()
            if email:
                user_dashboard(email)
        elif choice == "3":
            print("\nReturning to main portal...")
            break
        else:
            print("❌ Invalid option! Please enter 1-3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()