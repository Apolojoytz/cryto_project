# voting_system/main.py
from database.db_setup import setup_tables

def display_welcome():
    """Display welcome banner"""
    print("\n" + "="*50)
    print("        VOTING SYSTEM MANAGEMENT")
    print("="*50)
    print("Secure Online Voting Platform")
    print("="*50)

def main():
    """Main entry point"""
    # Setup database
    print("🔧 Initializing system...")
    if not setup_tables():
        print("❌ Failed to setup database. Please check MySQL/XAMPP is running.")
        input("Press Enter to exit...")
        return
    
    display_welcome()
    
    while True:
        print("\n" + "="*40)
        print("MAIN PORTAL")
        print("="*40)
        print("1. 👤 User Portal")
        print("2. 🛡️  Admin Portal")
        print("3. 🚪 Exit System")
        print("="*40)

        choice = input("\nChoose option (1-3): ").strip()

        if choice == "1":
            # Import and run user portal
            try:
                from user.main_user import main as user_main
                user_main()
            except ImportError as e:
                print(f"❌ Error loading user module: {e}")
                input("Press Enter to continue...")
                
        elif choice == "2":
            # Import and run admin portal
            try:
                from admin.main_admin import main as admin_main
                admin_main()
            except ImportError as e:
                print(f"❌ Error loading admin module: {e}")
                input("Press Enter to continue...")
                
        elif choice == "3":
            print("\n" + "="*40)
            print("Thank you for using the Voting System!")
            print("Goodbye! 👋")
            print("="*40)
            break
        else:
            print("❌ Invalid option! Please enter 1-3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()