# voting_system/force_blockchain_vote.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def force_record_vote():
    """Force record a vote on blockchain"""
    print("⛓️  FORCING BLOCKCHAIN VOTE RECORDING")
    print("="*50)
    
    try:
        from blockchain.voting_blockchain import voting_blockchain
        
        # Get existing votes from database
        from database.db_connection import execute_query
        
        query = """
        SELECT v.*, u.username, c.name as candidate_name, vs.name as session_name
        FROM votes v
        JOIN users u ON v.user_email = u.email
        JOIN candidates c ON v.candidate_id = c.id
        JOIN voting_sessions vs ON v.session_id = vs.id
        ORDER BY v.voted_at
        """
        
        votes = execute_query(query, fetch=True)
        
        if not votes:
            print("❌ No votes in database")
            return
        
        print(f"Found {len(votes)} votes in database")
        print("\n" + "="*50)
        
        for i, vote in enumerate(votes, 1):
            print(f"\n{i}. {vote['user_email']}")
            print(f"   Session: {vote['session_name']} (#{vote['session_id']})")
            print(f"   Candidate: {vote['candidate_name']}")
            print(f"   Time: {vote['voted_at']}")
            
            # Check if already on blockchain
            already_on_blockchain = False
            for block in voting_blockchain.blockchain.chain:
                if (block.data.get('type') == 'vote' and 
                    block.data.get('user_email_hash') == voting_blockchain.hash_email(vote['user_email']) and
                    block.data.get('session_id') == vote['session_id']):
                    already_on_blockchain = True
                    print(f"   ✅ Already on blockchain (Block #{block.index})")
                    break
            
            if not already_on_blockchain:
                print(f"   ❌ NOT on blockchain - adding now...")
                
                # Record on blockchain
                block_hash = voting_blockchain.record_vote(
                    vote['session_id'],
                    vote['user_email'],
                    vote['candidate_id'],
                    vote['candidate_name']
                )
                
                if block_hash:
                    print(f"   ✅ Added! Block hash: {block_hash[:16]}...")
                else:
                    print(f"   ❌ Failed to add")
        
        # Save blockchain
        voting_blockchain.blockchain.save_to_file()
        
        print("\n" + "="*50)
        print(f"✅ Final blockchain length: {len(voting_blockchain.blockchain.chain)} blocks")
        
        # Show vote blocks
        print("\n🗳️  Votes on blockchain:")
        vote_count = 0
        for block in voting_blockchain.blockchain.chain:
            if block.data.get('type') == 'vote':
                vote_count += 1
                print(f"  Block #{block.index}:")
                print(f"    User: {block.data.get('username', 'N/A')}")
                print(f"    Candidate: {block.data.get('candidate_name')}")
                print(f"    Session: {block.data.get('session_id')}")
        
        print(f"\n📊 Total votes on blockchain: {vote_count}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Make sure blockchain module exists:")
        print("   blockchain/")
        print("   ├── __init__.py")
        print("   ├── blockchain.py")
        print("   ├── voting_blockchain.py")
        print("   └── verification_tool.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_direct_recording():
    """Test blockchain recording directly"""
    print("\n🧪 Testing direct blockchain recording...")
    
    try:
        from blockchain.voting_blockchain import voting_blockchain
        
        print(f"Current blockchain: {len(voting_blockchain.blockchain.chain)} blocks")
        
        # Record a test vote
        test_hash = voting_blockchain.record_vote(
            session_id=100,
            user_email="direct_test@example.com",
            candidate_id=100,
            candidate_name="Direct Test"
        )
        
        if test_hash:
            print(f"✅ Direct test SUCCESS! Hash: {test_hash[:16]}...")
            print(f"   New blockchain: {len(voting_blockchain.blockchain.chain)} blocks")
            
            # Verify it's there
            found = False
            for block in voting_blockchain.blockchain.chain:
                if block.data.get('type') == 'vote' and block.hash == test_hash:
                    found = True
                    print(f"   ✅ Verified in block #{block.index}")
                    break
            
            if not found:
                print("   ❌ Test vote not found in blockchain!")
        else:
            print("❌ Direct test FAILED - record_vote() returned None")
            
    except Exception as e:
        print(f"❌ Direct test error: {e}")

if __name__ == "__main__":
    print("="*60)
    print("FORCE BLOCKCHAIN VOTE FIX")
    print("="*60)
    
    # First test direct recording
    test_direct_recording()
    
    # Then force record existing votes
    print("\n" + "="*60)
    print("PROCESSING EXISTING VOTES")
    print("="*60)
    
    force_record_vote()
    
    input("\nPress Enter to exit...")