# voting_system/admin/main_admin.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules - MAKE SURE THESE EXIST
from admin.auth.admin_login import admin_login
from admin.users.view_users import view_all_users
from admin.voting.create_voting import create_voting_session
from admin.voting.delete_voting import delete_voting_session
from admin.voting.view_results import view_voting_results
from admin.auth.admin_logout import admin_logout

# Try to import blockchain tools (they might not exist yet)
try:
    from blockchain.verification_tool import (
        verify_vote_on_blockchain, 
        view_blockchain_info, 
        audit_blockchain
    )
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    BLOCKCHAIN_AVAILABLE = False
    print("⚠️  Blockchain module not available")

# ADD THIS FUNCTION IF IT DOESN'T EXIST
def view_database_stats():
    """View database statistics - SIMPLE VERSION"""
    from database.db_connection import execute_query
    
    print("\n" + "="*60)
    print("📊 DATABASE STATISTICS")
    print("="*60)
    
    # Simple statistics
    stats = [
        ("Total Users", "SELECT COUNT(*) as count FROM users"),
        ("Verified Users", "SELECT COUNT(*) as count FROM users WHERE voting_verified = 1"),
        ("Voting Sessions", "SELECT COUNT(*) as count FROM voting_sessions"),
        ("Total Votes", "SELECT COUNT(*) as count FROM votes"),
    ]
    
    for label, query in stats:
        result = execute_query(query, fetch_one=True)
        if result:
            print(f"{label}: {result['count']}")
    
    print("="*60)
    input("\nPress Enter to continue...")

def display_admin_welcome():
    """Display admin welcome banner"""
    print("\n" + "="*50)
    print("         ADMIN PORTAL - VOTING SYSTEM")
    print("="*50)
    print("⚠️  Restricted Access - Admin Only")
    print("="*50)

def admin_dashboard():
    """Admin dashboard after login"""
    while True:
        print("\n" + "="*50)
        print("         ADMIN DASHBOARD")
        print("="*50)
        print("1. 👥 View All Users")
        print("2. 📊 View Database Statistics")
        print("3. 🗑️  Delete Voting Session")
        print("4. 🗳️  Create Voting Session")
        print("5. 📈 View Voting Results")
        
        # Only show blockchain if available
        if BLOCKCHAIN_AVAILABLE:
            print("6. ⛓️  Blockchain Tools")
            print("7. 🚪 Logout")
            total_options = 7
        else:
            print("6. 🚪 Logout")
            total_options = 6
        
        print("="*50)

        choice = input(f"\nChoose option (1-{total_options}): ").strip()

        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_database_stats()  # Now this exists!
        elif choice == "3":
            delete_voting_session()
        elif choice == "4":
            create_voting_session()
        elif choice == "5":
            view_voting_results()
        elif BLOCKCHAIN_AVAILABLE and choice == "6":
            blockchain_tools_menu()
        elif (not BLOCKCHAIN_AVAILABLE and choice == "6") or (BLOCKCHAIN_AVAILABLE and choice == "7"):
            admin_logout()
            break
        else:
            print(f"❌ Invalid option! Please enter 1-{total_options}.")
            input("Press Enter to continue...")

def blockchain_tools_menu():
    """Blockchain tools submenu - ONLY IF AVAILABLE"""
    if not BLOCKCHAIN_AVAILABLE:
        print("❌ Blockchain module not available")
        return
    
    while True:
        print("\n" + "="*40)
        print("⛓️  BLOCKCHAIN TOOLS")
        print("="*40)
        print("1. 🔍 Verify Specific Vote")
        print("2. 📊 View Blockchain Info")
        print("3. 📋 Audit Blockchain")
        print("4. ↩️  Back to Admin Dashboard")
        print("="*40)

        choice = input("\nChoose option (1-4): ").strip()

        if choice == "1":
            verify_vote_on_blockchain()
        elif choice == "2":
            view_blockchain_info()
        elif choice == "3":
            audit_blockchain()
        elif choice == "4":
            break
        else:
            print("❌ Invalid option! Please enter 1-4.")
            input("Press Enter to continue...")

def main():
    """Main entry point for admin portal"""
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