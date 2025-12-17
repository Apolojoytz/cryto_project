# voting_system/reset_blockchain.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import execute_query
from blockchain.blockchain_core import VotingBlockchain
import json

def reset_blockchain():
    """Reset blockchain and migrate votes fresh"""
    print("🔄 RESETTING BLOCKCHAIN")
    print("="*60)
    
    confirm = input("⚠️  This will DELETE ALL blockchain data and start fresh. Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Cancelled")
        return
    
    # Delete all blockchain data
    print("\n1. Deleting old blockchain data...")
    execute_query("DELETE FROM blockchain_blocks")
    print("✅ Deleted old blockchain blocks")
    
    # Create fresh blockchain
    print("\n2. Creating fresh blockchain...")
    fresh_blockchain = VotingBlockchain(difficulty=4)
    
    # Clear the default genesis block
    fresh_blockchain.chain = []
    fresh_blockchain.pending_votes = []
    
    # Create proper genesis block
    print("3. Creating genesis block...")
    fresh_blockchain.create_genesis_block()
    
    # Get all votes from database
    print("\n4. Getting all votes from database...")
    query = """
    SELECT v.*, u.username, c.name as candidate_name, vs.name as session_name
    FROM votes v
    JOIN users u ON v.user_email = u.email
    JOIN candidates c ON v.candidate_id = c.id
    JOIN voting_sessions vs ON v.session_id = vs.id
    ORDER BY v.id
    """
    votes = execute_query(query, fetch=True)
    
    if not votes:
        print("❌ No votes found")
        return
    
    print(f"✅ Found {len(votes)} votes")
    
    # Add all votes to blockchain
    print("\n5. Adding votes to blockchain...")
    import hashlib
    
    for i, vote in enumerate(votes, 1):
        # Create vote hash
        vote_string = f"{vote['id']}:{vote['user_email']}:{vote['candidate_id']}:{vote['voted_at']}"
        vote_hash = hashlib.sha256(vote_string.encode()).hexdigest()
        
        # Create vote data
        vote_data = {
            'vote_id': vote['id'],
            'user_email': vote['user_email'],
            'username': vote['username'],
            'candidate_id': vote['candidate_id'],
            'candidate_name': vote['candidate_name'],
            'session_id': vote['session_id'],
            'session_name': vote['session_name'],
            'timestamp': str(vote['voted_at']),
            'vote_hash': vote_hash
        }
        
        # Add to pending votes
        fresh_blockchain.pending_votes.append(vote_data)
        
        # Create a block (one block per vote for simplicity)
        fresh_blockchain.create_block_from_pending()
        
        print(f"  ✅ Added vote #{vote['id']} to blockchain ({i}/{len(votes)})")
    
    print("\n" + "="*60)
    print("✅ BLOCKCHAIN RESET COMPLETE")
    print(f"   Total blocks: {len(fresh_blockchain.chain)}")
    print(f"   Total votes in blockchain: {len(votes)}")
    
    # Test verification
    if votes:
        test_vote_id = votes[0]['id']
        result = fresh_blockchain.verify_vote(test_vote_id)
        
        print(f"\n🔍 Test verification for vote #{test_vote_id}:")
        if result and result['in_blockchain']:
            print("   ✅ Vote verified in blockchain")
        else:
            print("   ❌ Vote NOT in blockchain")
    
    print("="*60)
    input("Press Enter to continue...")

if __name__ == "__main__":
    reset_blockchain()