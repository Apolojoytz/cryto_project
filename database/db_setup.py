# voting_system/database/db_setup.py
from database.db_connection import execute_query
from config import DB_CONFIG
import mysql.connector
from mysql.connector import Error

def create_database():
    """Create database if it doesn't exist"""
    config = DB_CONFIG.copy()
    database = config.pop('database')
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        print(f"✅ Database '{database}' created/verified")
        
        cursor.close()
        connection.close()
        
        # Reconnect with database selected
        config['database'] = database
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        return connection, cursor
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return None, None


def setup_tables():
    """Create all necessary tables"""
    print("🔧 Setting up database tables...")
    # Create database first
    connection, cursor = create_database()
    if not connection:
        return False
    
    try:
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email_verified BOOLEAN DEFAULT FALSE,
            voting_verified BOOLEAN DEFAULT FALSE,
            has_voted BOOLEAN DEFAULT FALSE,
            voted_for VARCHAR(255),
            vote_time DATETIME,
            voted_session_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Created 'users' table")
        
        # Voting verification table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS voting_verification (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            fullname VARCHAR(255) NOT NULL,
            gender VARCHAR(50),
            phone VARCHAR(20),
            id_card_path VARCHAR(500),
            verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        )
        """)
        print("✅ Created 'voting_verification' table")
        
        # Voting sessions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS voting_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            start_date DATE,
            start_time TIME,
            end_date DATE,
            end_time TIME,
            duration_minutes INT,
            status VARCHAR(50) DEFAULT 'upcoming',
            total_votes INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Created 'voting_sessions' table")
        
        # Candidates table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(50),
            position VARCHAR(255),
            votes INT DEFAULT 0,
            FOREIGN KEY (session_id) REFERENCES voting_sessions(id) ON DELETE CASCADE
        )
        """)
        print("✅ Created 'candidates' table")
        
        # Votes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            user_email VARCHAR(255) NOT NULL,
            candidate_id INT NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES voting_sessions(id) ON DELETE CASCADE,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_session (session_id, user_email)
        )
        """)
        print("✅ Created 'votes' table")
        
        # OTP table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp_codes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            otp_code VARCHAR(10) NOT NULL,
            purpose VARCHAR(50),
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_email (email),
            INDEX idx_expires (expires_at)
        )
        """)
        print("✅ Created 'otp_codes' table")
        
        connection.commit()
        print("\n✅ All tables created successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        cursor.close()
        connection.close()