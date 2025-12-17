# voting_system/admin/blockchain/blockchain_tools.py
from blockchain.vote_verification import verify_specific_vote
from blockchain.audit_tools import view_blockchain_info, audit_blockchain
from blockchain.repair_tools import repair_blockchain
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def migrate_votes():
    """Migrate existing votes to blockchain"""
    try:
        from migrate_votes_to_blockchain import migrate_existing_votes
        migrate_existing_votes()
    except ImportError:
        print("❌ Migration script not found")
        input("Press Enter to continue...")

def blockchain_tools_menu():
    """Blockchain tools menu"""
    while True:
        print("\n" + "="*50)
        print("⛓️  BLOCKCHAIN TOOLS")
        print("="*50)
        print("1. 🔍 Verify Specific Vote")
        print("2. 📊 View Blockchain Info")
        print("3. 📋 Audit Blockchain")
        print("4. 🔄 Migrate Existing Votes")
        print("5. 🔧 Repair Blockchain")  # NEW OPTION
        print("6. ↩️  Back to Admin Dashboard")
        print("="*50)

        choice = input("\nChoose option (1-6): ").strip()

        if choice == "1":
            verify_specific_vote()
        elif choice == "2":
            view_blockchain_info()
        elif choice == "3":
            audit_blockchain()
        elif choice == "4":
            migrate_votes()
        elif choice == "5":
            repair_blockchain()
        elif choice == "6":
            print("\nReturning to admin dashboard...")
            break
        else:
            print("❌ Invalid option! Please enter 1-6.")
            input("Press Enter to continue...")