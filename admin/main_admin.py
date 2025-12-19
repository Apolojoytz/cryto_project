# voting_system/admin/main_admin.py - Updated dashboard
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin.auth.admin_login import admin_login
from admin.users.view_users import view_all_users
from admin.voting.create_voting import create_voting_session
from admin.voting.delete_voting import delete_voting_session
from admin.voting.view_results import view_voting_results
from admin.auth.admin_logout import admin_logout
from admin.stats.database_stats import view_database_statistics

# Try to import blockchain tools
try:
    from admin.blockchain.blockchain_tools import blockchain_tools_menu
    BLOCKCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Blockchain module not fully available: {e}")
    BLOCKCHAIN_AVAILABLE = False
except Exception as e:
    print(f"⚠️  Error loading blockchain module: {e}")
    BLOCKCHAIN_AVAILABLE = False

def display_admin_welcome():
    """Display admin welcome banner"""
    print("\n" + "="*50)
    print("         ADMIN PORTAL - VOTING SYSTEM")
    print("="*50)
    print("⚠️  Restricted Access - Admin Only")
    print("="*50)

def admin_dashboard():
    """Admin dashboard after login - UPDATED"""
    while True:
        print("\n" + "="*50)
        print("         ADMIN DASHBOARD")
        print("="*50)
        print("1. 👥 View All Users")
        print("2. 📊 View Database Statistics")
        print("3. 🗑️  Delete Voting Session")
        print("4. 🗳️  Create Voting Session")
        print("5. 📈 View Voting Results")
        
        if BLOCKCHAIN_AVAILABLE:
            print("6. ⛓️  Blockchain Tools")  
            print("7. 🚪 Logout")
            option_count = 7
        else:
            print("6. 🚪 Logout")
            option_count = 6
        
        print("="*50)

        choice = input(f"\nChoose option (1-{option_count}): ").strip()

        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_database_statistics()
        elif choice == "3":
            delete_voting_session()
        elif choice == "4":
            create_voting_session()
        elif choice == "5":
            view_voting_results()
        elif BLOCKCHAIN_AVAILABLE and choice == "6":
            blockchain_tools_menu()
        elif (BLOCKCHAIN_AVAILABLE and choice == "7") or (not BLOCKCHAIN_AVAILABLE and choice == "6"):
            admin_logout()
            break
        else:
            print(f"❌ Invalid option! Please enter 1-{option_count}.")
            input("Press Enter to continue...")

def main():
    display_admin_welcome()
    
    while True:
        print("\n" + "="*40)
        print("ADMIN MENU")
        print("="*40)
        print("1. 🔐 Admin Login")
        print("2. ↩️  Back to Main Portal")
        print("="*40)

        choice = input("\nChoose option (1-2): ").strip()

        if choice == "1":
            email = admin_login()
            if email:
                admin_dashboard()
        elif choice == "2":
            print("\nReturning to main portal...")
            break
        else:
            print("❌ Invalid option! Please enter 1-2.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()