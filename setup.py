import os
import json

def create_directory_structure():
    """Create the complete directory structure"""
    directories = [
        "Database/blockchain",
        "Database/id_cards",
        "user",
        "admin"
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    return True

def create_init_files():
    """Create __init__.py files"""
    init_files = [
        "user/__init__.py",
        "admin/__init__.py",
        "Database/blockchain/__init__.py"
    ]
    
    print("\nCreating package files...")
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
            print(f"  ✓ {init_file}")
    
    return True

def create_empty_database_files():
    """Create empty database files"""
    database_files = [
        ("Database/users.json", {}),
        ("Database/voting_data.json", {}),
        ("Database/voting_sessions.json", [])
    ]
    
    print("\nCreating database files...")
    for file_path, default_data in database_files:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(default_data, f, indent=2)
            print(f"  ✓ {file_path}")
    
    return True

def initialize_blockchain():
    """Initialize the blockchain"""
    print("\n" + "="*60)
    print("BLOCKCHAIN INITIALIZATION")
    print("="*60)
    
    # Import after setting up paths
    import sys
    sys.path.append('.')
    from config import get_blockchain
    
    blockchain = get_blockchain()
    
    print("✅ Blockchain initialized successfully!")
    print(f"   Genesis block created")
    print(f"   Difficulty level: {blockchain.difficulty}")
    print(f"   Ledger file: Database/blockchain/ledger.json")
    print("="*60)

def main():
    """Main setup function"""
    print("="*60)
    print("ONLINE VOTING SYSTEM - SETUP WITH BLOCKCHAIN")
    print("="*60)
    
    # Create structure
    create_directory_structure()
    create_init_files()
    create_empty_database_files()
    
    # Initialize blockchain
    initialize_blockchain()
    
    print("\n📁 Project Structure Created:")
    print("  ├── main.py              # Main entry point")
    print("  ├── config.py            # Configuration")
    print("  ├── setup.py             # This setup script")
    print("  ├── Database/")
    print("  │   ├── blockchain/      # Blockchain implementation")
    print("  │   │   ├── block.py     # Block class")
    print("  │   │   ├── blockchain.py # Blockchain class")
    print("  │   │   └── ledger.json  # Blockchain ledger")
    print("  │   ├── users.json       # User database")
    print("  │   ├── voting_data.json # Voting data")
    print("  │   ├── voting_sessions.json # Voting sessions")
    print("  │   └── id_cards/        # User ID cards")
    print("  ├── user/                # User portal")
    print("  └── admin/               # Admin portal")
    
    print("\n🚀 To run the system:")
    print("   python main.py")
    
    print("\n🔗 BLOCKCHAIN FEATURES:")
    print("   1. All transactions recorded on immutable blockchain")
    print("   2. User registrations tracked")
    print("   3. Voting verifications recorded")
    print("   4. Every vote permanently stored")
    print("   5. Voting sessions creation logged")
    print("   6. Blockchain explorer in admin panel")
    print("   7. Integrity verification")
    print("="*60)

if __name__ == "__main__":
    main()