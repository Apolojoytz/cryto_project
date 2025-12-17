from database.db_connection import execute_query
from .blockchain_core import blockchain
import json
import hashlib

def add_vote_to_blockchain(vote_id, email, candidate_id, session_id):
    """Add a vote to the blockchain"""
    # Get vote details
    query = """
    SELECT v.*, u.username, c.name as candidate_name, vs.name as session_name
    FROM votes v
    JOIN users u ON v.user_email = u.email
    JOIN candidates c ON v.candidate_id = c.id
    JOIN voting_sessions vs ON v.session_id = vs.id
    WHERE v.id = %s
    """
    vote = execute_query(query, (vote_id,), fetch_one=True)
    
    if not vote:
        return False
    
    # Create vote hash for integrity
    vote_string = f"{vote_id}:{email}:{candidate_id}:{vote['voted_at']}"
    vote_hash = hashlib.sha256(vote_string.encode()).hexdigest()
    
    # Create blockchain vote data
    vote_data = {
        'vote_id': vote_id,
        'user_email': email,
        'username': vote['username'],
        'candidate_id': candidate_id,
        'candidate_name': vote['candidate_name'],
        'session_id': session_id,
        'session_name': vote['session_name'],
        'timestamp': str(vote['voted_at']),
        'vote_hash': vote_hash
    }
    
    # Add to blockchain
    blockchain.add_vote_to_blockchain(vote_data)
    
    return True

def verify_specific_vote():
    """Verify a specific vote in the blockchain"""
    print("\n" + "="*50)
    print("🔍 VERIFY SPECIFIC VOTE")
    print("="*50)
    
    try:
        vote_id = int(input("Enter Vote ID to verify: ").strip())
    except ValueError:
        print("❌ Please enter a valid numeric Vote ID")
        input("Press Enter to continue...")
        return
    
    result = blockchain.verify_vote(vote_id)
    
    if not result:
        print("❌ Vote not found!")
        input("Press Enter to continue...")
        return
    
    vote = result['vote_details']
    
    print(f"\n📋 VOTE DETAILS:")
    print(f"   Vote ID: {vote['id']}")
    print(f"   User: {vote['username']} ({vote['user_email']})")
    print(f"   Candidate: {vote['candidate_name']}")
    print(f"   Session: {vote['session_name']}")
    print(f"   Time: {vote['voted_at']}")
    
    print(f"\n⛓️  BLOCKCHAIN VERIFICATION:")
    if result['in_blockchain']:
        print("   ✅ Vote is recorded in blockchain")
        print(f"   Block Index: {result['blockchain_data']['block_index']}")
        print(f"   Block Hash: {result['blockchain_data']['block_hash'][:20]}...")
        print(f"   Block Time: {result['blockchain_data']['block_timestamp']}")
        
        if result['integrity_verified']:
            print("   🔒 Vote integrity: ✅ VERIFIED")
        else:
            print("   🔒 Vote integrity: ❌ TAMPERED")
    else:
        print("   ❌ Vote is NOT in blockchain (unverified)")
    
    print("="*50)
    input("\nPress Enter to continue...")