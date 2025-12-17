# voting_system/config.py
import os

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'voting_system_db',
    'port': 3306
}

# Get database path for SQLite/blockchain
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "voting_system.db")  # ADD THIS LINE

# Blockchain Configuration - FIXED: Use BASE_DIR instead of DB_PATH
BLOCKCHAIN_CONFIG = {
    'difficulty': 4,
    'blockchain_file': os.path.join(BASE_DIR, 'blockchain', 'blockchain.json'),  # FIXED
    'audit_log_enabled': True,
    'hash_salt': 'voting_system_salt_2024'
}

# ... rest of your existing config ...

# Admin credentials (hardcoded)
ADMIN_EMAIL = "naninina2k24@gmail.com"
ADMIN_PASSWORD = "HeloCyber55Hack<3LoynasAhloy992005"

# Email configuration for OTP
GMAIL_SENDER = "naninina2k24@gmail.com"  # Change this
GMAIL_APP_PASSWORD = "dcnl dqho nquz afwa"   # CHANGE THIS

# OTP configuration
OTP_EXPIRY_MINUTES = 10

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ID_CARD_FOLDER = os.path.join(UPLOAD_FOLDER, 'id_cards')
os.makedirs(ID_CARD_FOLDER, exist_ok=True)