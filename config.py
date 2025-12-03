import os

# Base directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "Database")
USER_DIR = os.path.join(BASE_DIR, "user")
ADMIN_DIR = os.path.join(BASE_DIR, "admin")
BLOCKCHAIN_DIR = os.path.join(DATABASE_DIR, "blockchain")

# File paths
DB_FILE = os.path.join(DATABASE_DIR, "users.json")
VOTING_FILE = os.path.join(DATABASE_DIR, "voting_data.json")
VOTING_SESSIONS_FILE = os.path.join(DATABASE_DIR, "voting_sessions.json")
ID_CARD_FOLDER = os.path.join(DATABASE_DIR, "id_cards")
BLOCKCHAIN_LEDGER = os.path.join(BLOCKCHAIN_DIR, "ledger.json")

# Email configuration
GMAIL_SENDER = "naninina2k24@gmail.com"
GMAIL_APP_PASSWORD = "dcnl dqho nquz afwa"

# Admin credentials
ADMIN_EMAIL = "naninina2k24@gmail.com"
ADMIN_PASSWORD = "HeloCyber55Hack<3LoynasAhloy992005"

# Blockchain settings
BLOCKCHAIN_DIFFICULTY = 3  # Lower difficulty for faster mining

# Create necessary directories
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(ID_CARD_FOLDER, exist_ok=True)
os.makedirs(BLOCKCHAIN_DIR, exist_ok=True)

# Create empty JSON files if they don't exist
def initialize_database():
    """Initialize database files if they don't exist"""
    files_to_create = [
        (DB_FILE, '{}'),
        (VOTING_FILE, '{}'),
        (VOTING_SESSIONS_FILE, '[]'),
    ]
    
    for file_path, default_content in files_to_create:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(default_content)

# Initialize blockchain
def initialize_blockchain():
    """Initialize the blockchain"""
    from Database.blockchain.blockchain import VotingBlockchain
    blockchain = VotingBlockchain(BLOCKCHAIN_LEDGER)
    return blockchain

# Initialize on import
initialize_database()

# Global blockchain instance (singleton pattern)
_blockchain_instance = None

def get_blockchain():
    """Get or create blockchain instance"""
    global _blockchain_instance
    if _blockchain_instance is None:
        _blockchain_instance = initialize_blockchain()
    return _blockchain_instance

# Helper functions for regular file operations (for backward compatibility)
def load_json(path):
    """Load JSON file (for regular files, not blockchain)"""
    import json
    if not os.path.exists(path):
        if 'sessions' in path:
            return []
        return {}
    if os.path.getsize(path) == 0:
        if 'sessions' in path:
            return []
        return {}
    try:
        return json.load(open(path, "r"))
    except:
        if 'sessions' in path:
            return []
        return {}

def save_json(path, data):
    """Save JSON file (for regular files, not blockchain)"""
    import json
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return True