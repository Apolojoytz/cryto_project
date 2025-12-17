# voting_system/config.py
import os

# MySQL/MariaDB Database Configuration (XAMPP)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # XAMPP default is empty password
    'database': 'voting_system_db',
    'port': 3306,
    'charset': 'utf8mb4'
}

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