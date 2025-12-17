# voting_system/setup.py
from database.db_setup import setup_tables
import mysql.connector
from config import DB_CONFIG

def check_mysql_connection():
    """Check if MySQL/XAMPP is running"""
    try:
        config = DB_CONFIG.copy()
        # Try to connect without database first
        config.pop('database', None)
        
        connection = mysql.connector.connect(**config)
        print("✅ Connected to MySQL server")
        connection.close()
        return True
    except mysql.connector.Error as e:
        print(f"❌ Cannot connect to MySQL: {e}")
        print("\nPlease ensure:")
        print("1. XAMPP is installed and running")
        print("2. MySQL service is started in XAMPP Control Panel")
        print("3. Default credentials: user='root', password='' (empty)")
        return False

def main():
    """Setup the voting system"""
    print("="*50)
    print("VOTING SYSTEM SETUP")
    print("="*50)
    
    # Check MySQL connection
    if not check_mysql_connection():
        input("\nPress Enter to exit...")
        return
    
    # Setup database and tables
    print("\n🔧 Setting up database...")
    if setup_tables():
        print("\n✅ Setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Update email credentials in config.py")
        print("   - GMAIL_SENDER = 'your_email@gmail.com'")
        print("   - GMAIL_APP_PASSWORD = 'your_app_password'")
        print("2. Run the system: python main.py")
    else:
        print("\n❌ Setup failed!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()