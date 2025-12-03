import json
from config import DB_FILE, VOTING_SESSIONS_FILE, get_blockchain, load_json

def view_results():
    """View voting results with blockchain verification"""
    print("\n" + "="*50)
    print("VOTING RESULTS WITH BLOCKCHAIN VERIFICATION")
    print("="*50)
    
    db = load_json(DB_FILE)
    sessions = load_json(VOTING_SESSIONS_FILE)
    blockchain = get_blockchain()
    
    # Overall statistics
    total_users = len(db)
    voted_users = sum(1 for user in db.values() if user.get('has_voted', False))
    voting_verified = sum(1 for user in db.values() if user.get('voting_verified', False))
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Total Registered Users: {total_users}")
    print(f"   Voting Verified Users: {voting_verified}")
    print(f"   Users Who Have Voted: {voted_users}")
    
    if total_users > 0:
        voter_percentage = (voted_users / total_users) * 100
        print(f"   Voter Turnout: {voter_percentage:.1f}%")
    
    # Get votes from blockchain for verification
    blockchain_votes = blockchain.get_voting_results()
    print(f"\n📗 BLOCKCHAIN VERIFICATION:")
    print(f"   Total votes on blockchain: {len(blockchain_votes)}")
    
    # Check blockchain validity
    try:
        is_valid = blockchain.is_chain_valid()
        print(f"   Blockchain valid: {'✅ Yes' if is_valid else '❌ No'}")
    except:
        print(f"   Blockchain valid: ⚠️ Could not verify")
    
    # Session-based results
    if sessions:
        print(f"\n📋 VOTING SESSIONS RESULTS:")
        print("-" * 50)
        
        for session in sessions:
            print(f"\n🗳️  Session #{session['id']}: {session['name']}")
            print(f"   Status: {session['status'].upper()}")
            print(f"   Database Votes: {session['total_votes']}")
            
            # Get blockchain votes for this session
            session_blockchain_votes = []
            try:
                session_blockchain_votes = blockchain.get_voting_results(session['id'])
                print(f"   Blockchain Votes: {len(session_blockchain_votes)}")
                
                # Verify consistency
                if session['total_votes'] == len(session_blockchain_votes):
                    print(f"   ✅ Votes consistent with blockchain")
                else:
                    print(f"   ⚠️  Votes mismatch! Check blockchain for verification")
            except:
                print(f"   Blockchain Votes: ⚠️ Could not retrieve")
            
            if session['candidates']:
                # Sort candidates by votes (descending)
                sorted_candidates = sorted(session['candidates'], 
                                         key=lambda x: x['votes'], 
                                         reverse=True)
                
                print("   Results:")
                for i, candidate in enumerate(sorted_candidates, 1):
                    if session['total_votes'] > 0:
                        percentage = (candidate['votes'] / session['total_votes']) * 100
                    else:
                        percentage = 0
                    
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                    print(f"     {medal} {candidate['name']}: {candidate['votes']} votes ({percentage:.1f}%)")
                
                # Announce winner if there are votes
                if sorted_candidates and session['total_votes'] > 0:
                    winner = sorted_candidates[0]
                    print(f"\n   🎉 WINNER: {winner['name']} with {winner['votes']} votes!")
    
    print("="*50)
    input("\nPress Enter to continue...")