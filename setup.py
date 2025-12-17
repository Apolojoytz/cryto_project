# voting_system/setup.py
from database.db_setup import setup_tables
import mysql.connector
from config import DB_CONFIG
# create_missing_table.py
from database.db_connection import execute_query
def create_blockchain_references_table():
    """Create blockchain_references table after database exists"""
    query = """
    CREATE TABLE IF NOT EXISTS blockchain_references (
        id INT AUTO_INCREMENT PRIMARY KEY,
        block_hash VARCHAR(255) NOT NULL,
        record_type VARCHAR(50) NOT NULL,
        identifier VARCHAR(255) NOT NULL,
        reference_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_block_hash (block_hash),
        INDEX idx_identifier (identifier),
        INDEX idx_record_type (record_type)
    )
    """

    return execute_query(query)
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
        print("🔧 Creating blockchain reference table...")
        result = create_blockchain_references_table()

        if result:
            print("✅ Created 'blockchain_references' table")
        else:
            print("❌ Failed to create 'blockchain_references' table")

        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()