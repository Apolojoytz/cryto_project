# voting_system/admin/blockchain/blockchain_tools.py
from blockchain.vote_verification import verify_specific_vote
from blockchain.audit_tools import view_blockchain_info, audit_blockchain
from blockchain.secure_results import show_blockchain_verified_results, verify_all_election_results
from blockchain.blockchain_repair import fix_database_votes_from_blockchain
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def blockchain_tools_menu():
    """Blockchain tools menu - UPDATED VERSION"""
    while True:
        print("\n" + "="*50)
        print("⛓️  BLOCKCHAIN TOOLS")
        print("="*50)
        print("1. 🔍 Verify Specific Vote")
        print("2. 📊 View Blockchain Info")
        print("3. 📋 Audit Blockchain")
        print("4. 🏆 View Blockchain-Verified Results")  
        print("5. 🔍 Verify All Results Integrity")      
        print("6. 🔧 Fix Database from Blockchain")      
        print("7. ↩️  Back to Admin Dashboard")
        print("="*50)

        choice = input("\nChoose option (1-7): ").strip()

        if choice == "1":
            verify_specific_vote()
        elif choice == "2":
            view_blockchain_info()
        elif choice == "3":
            audit_blockchain()
        elif choice == "4":  
            show_blockchain_verified_results()
        elif choice == "5":  
            verify_all_election_results()
        elif choice == "6":  
            fix_database_votes_from_blockchain()
        elif choice == "7":
            print("\nReturning to admin dashboard...")
            break
        else:
            print("❌ Invalid option! Please enter 1-7.")
            input("Press Enter to continue...")