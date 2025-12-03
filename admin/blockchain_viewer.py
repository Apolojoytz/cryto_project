import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config import get_blockchain

def view_blockchain():
    """View the blockchain ledger"""
    blockchain = get_blockchain()
    
    while True:
        print("\n" + "="*60)
        print("BLOCKCHAIN EXPLORER")
        print("="*60)
        print("1. 📋 View Blockchain Summary")
        print("2. 🔍 View All Transactions")
        print("3. 👤 View User Transactions")
        print("4. 🗳️  View All Votes")
        print("5. 📊 View Session Votes")
        print("6. ✅ Verify Blockchain Integrity")
        print("7. ↩️  Back to Admin Menu")
        print("="*60)

        choice = input("\nChoose option (1-7): ").strip()

        if choice == "1":
            blockchain.print_blockchain_summary()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            blockchain.print_chain_details()
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            email = input("Enter user email: ").strip().lower()
            transactions = blockchain.get_user_transactions(email)
            
            print(f"\n" + "="*80)
            print(f"BLOCKCHAIN TRANSACTIONS FOR: {email}")
            print("="*80)
            
            if not transactions:
                print("No transactions found for this user.")
            else:
                for tx in transactions:
                    print(f"\nBlock #{tx['block']}")
                    print(f"  Type: {tx['type'].upper()}")
                    print(f"  Time: {tx['timestamp']}")
                    print(f"  TX ID: {tx['transaction_id']}")
                    
                    data = tx['data']
                    if tx['type'] == 'vote':
                        print(f"  Candidate: {data.get('candidate_name')}")
                        print(f"  Session: {data.get('session_id')}")
                        print(f"  Vote ID: {data.get('vote_id')}")
                    elif tx['type'] == 'registration':
                        print(f"  Username: {data.get('username')}")
                        print(f"  User ID: {data.get('user_id')}")
                    elif tx['type'] == 'verification':
                        print(f"  Full Name: {data.get('fullname')}")
                        print(f"  ID Card Hash: {data.get('id_card_hash')}")
            
            print(f"\nTotal Transactions: {len(transactions)}")
            print("="*80)
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            votes = blockchain.get_voting_results()
            print("\n" + "="*80)
            print("ALL VOTES ON BLOCKCHAIN")
            print("="*80)
            
            if not votes:
                print("No votes recorded yet.")
            else:
                # Count votes per candidate
                candidate_votes = {}
                for vote in votes:
                    candidate = vote['candidate']
                    candidate_votes[candidate] = candidate_votes.get(candidate, 0) + 1
                
                print("\n📊 VOTE DISTRIBUTION:")
                for candidate, count in candidate_votes.items():
                    percentage = (count / len(votes)) * 100
                    print(f"  {candidate}: {count} votes ({percentage:.1f}%)")
                
                print(f"\n📋 DETAILED VOTES ({len(votes)} total):")
                for vote in votes[:10]:  # Show first 10
                    print(f"\n  Block #{vote['block']}")
                    print(f"    Voter: {vote['voter']}")
                    print(f"    Candidate: {vote['candidate']}")
                    print(f"    Session: {vote['session']}")
                    print(f"    Time: {vote['timestamp']}")
                
                if len(votes) > 10:
                    print(f"\n  ... and {len(votes) - 10} more votes")
            
            print("="*80)
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            session_id = input("Enter session ID: ").strip()
            if session_id.isdigit():
                votes = blockchain.get_voting_results(session_id=int(session_id))
                
                print(f"\n" + "="*80)
                print(f"BLOCKCHAIN VOTES FOR SESSION #{session_id}")
                print("="*80)
                
                if not votes:
                    print("No votes found for this session.")
                else:
                    # Count votes per candidate
                    candidate_votes = {}
                    for vote in votes:
                        candidate = vote['candidate']
                        candidate_votes[candidate] = candidate_votes.get(candidate, 0) + 1
                    
                    print("\n📊 RESULTS FROM BLOCKCHAIN:")
                    for candidate, count in candidate_votes.items():
                        percentage = (count / len(votes)) * 100
                        print(f"  {candidate}: {count} votes ({percentage:.1f}%)")
                    
                    # Find winner
                    if candidate_votes:
                        winner = max(candidate_votes.items(), key=lambda x: x[1])
                        print(f"\n  🎉 BLOCKCHAIN WINNER: {winner[0]} with {winner[1]} votes")
                    
                    print(f"\n  Total votes on blockchain: {len(votes)}")
                
                print("="*80)
            else:
                print("❌ Invalid session ID!")
            
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            print("\n" + "="*60)
            print("BLOCKCHAIN INTEGRITY CHECK")
            print("="*60)
            
            is_valid = blockchain.is_chain_valid()
            total_blocks = len(blockchain.chain)
            total_transactions = total_blocks - 1  # Excluding genesis
            
            print(f"Total Blocks: {total_blocks}")
            print(f"Total Transactions: {total_transactions}")
            print(f"Chain Valid: {'✅ YES' if is_valid else '❌ NO'}")
            
            if is_valid:
                print("\n✅ Blockchain integrity verified successfully!")
                print("   All blocks are properly linked.")
                print("   All hashes are valid.")
                print("   Proof of Work verified.")
            else:
                print("\n❌ WARNING: Blockchain integrity check failed!")
                print("   The chain may have been tampered with!")
            
            print("="*60)
            input("\nPress Enter to continue...")
            
        elif choice == "7":
            break
            
        else:
            print("❌ Invalid option! Please enter 1-7.")

def main():
    """Main function for blockchain viewer"""
    view_blockchain()

if __name__ == "__main__":
    main()