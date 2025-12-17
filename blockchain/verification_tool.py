# voting_system/blockchain/verification_tool.py
from .voting_blockchain import voting_blockchain
from database.db_connection import execute_query

def verify_vote_on_blockchain():
    """Verify a specific vote on blockchain"""
    print("\n" + "="*40)
    print("🔍 VERIFY VOTE ON BLOCKCHAIN")
    print("="*40)
    
    email = input("Enter user email: ").strip().lower()
    session_id = input("Enter session ID: ").strip()
    
    try:
        session_id = int(session_id)
    except ValueError:
        print("❌ Invalid session ID")
        input("Press Enter to continue...")
        return
    
    print("\n🔎 Searching blockchain...")
    result = voting_blockchain.verify_vote(email, session_id)
    
    if result["found"]:
        print("\n✅ VOTE VERIFIED ON BLOCKCHAIN!")
        print("="*40)
        print(f"Block Index: {result['block_index']}")
        print(f"Block Hash: {result['block_hash']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Candidate: {result['candidate']}")
        print(f"Session ID: {session_id}")
        print("="*40)
        
        # Also check database for consistency
        db_query = """
        SELECT v.*, u.username, c.name as candidate_name
        FROM votes v
        JOIN users u ON v.user_email = u.email
        JOIN candidates c ON v.candidate_id = c.id
        WHERE v.user_email = %s AND v.session_id = %s
        """
        db_result = execute_query(db_query, (email, session_id), fetch_one=True)
        
        if db_result:
            print("\n📊 DATABASE RECORD:")
            print(f"Candidate: {db_result['candidate_name']}")
            print(f"Vote Time: {db_result['voted_at']}")
            print("✅ Database and blockchain records match!")
        else:
            print("⚠️  Vote found on blockchain but not in database!")
    else:
        print("\n❌ Vote not found on blockchain")
    
    input("\nPress Enter to continue...")

def view_blockchain_info():
    """View blockchain information"""
    print("\n" + "="*40)
    print("⛓️  BLOCKCHAIN INFORMATION")
    print("="*40)
    
    info = voting_blockchain.get_blockchain_info()
    
    print(f"Chain Length: {info['chain_length']} blocks")
    print(f"Blockchain Valid: {'✅ Yes' if info['is_valid'] else '❌ No'}")
    print(f"Mining Difficulty: {info['difficulty']}")
    
    if info['latest_block']:
        print(f"\n📦 Latest Block (#{info['latest_block']['index']}):")
        print(f"   Hash: {info['latest_block']['hash'][:32]}...")
        print(f"   Timestamp: {info['latest_block']['timestamp']}")
        print(f"   Data Type: {info['latest_block']['data'].get('type', 'N/A')}")
    
    # Show vote statistics
    validation = voting_blockchain.validate_all_votes()
    print(f"\n🗳️  Votes on Blockchain: {validation['total_votes']}")
    print(f"Blockchain Integrity: {'✅ Valid' if validation['blockchain_valid'] else '❌ Invalid'}")
    
    print("="*40)
    input("\nPress Enter to continue...")

def audit_blockchain():
    """Audit the entire blockchain"""
    print("\n" + "="*40)
    print("📋 BLOCKCHAIN AUDIT")
    print("="*40)
    
    print("🔍 Validating blockchain...")
    
    if voting_blockchain.blockchain.is_chain_valid():
        print("✅ Blockchain integrity: VALID")
    else:
        print("❌ Blockchain integrity: INVALID")
        print("   Blockchain has been tampered with!")
    
    # Count by type
    type_count = {}
    for block in voting_blockchain.blockchain.chain:
        block_type = block.data.get("type", "unknown")
        type_count[block_type] = type_count.get(block_type, 0) + 1
    
    print("\n📊 Block Types:")
    for block_type, count in type_count.items():
        print(f"   {block_type}: {count} blocks")
    
    # Show all votes
    print("\n🗳️  All Votes on Blockchain:")
    print("-" * 40)
    
    votes = []
    for block in voting_blockchain.blockchain.chain:
        if block.data.get("type") == "vote":
            votes.append({
                "block": block.index,
                "session": block.data.get("session_id"),
                "candidate": block.data.get("candidate_name"),
                "timestamp": block.timestamp
            })
    
    if votes:
        for vote in votes:
            print(f"Block #{vote['block']}:")
            print(f"  Session: {vote['session']}")
            print(f"  Candidate: {vote['candidate']}")
            print(f"  Time: {vote['timestamp']}")
            print()
    else:
        print("No votes recorded yet.")
    
    print(f"Total votes on chain: {len(votes)}")
    print("="*40)
    input("\nPress Enter to continue...")