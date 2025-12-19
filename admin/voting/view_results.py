# voting_system/admin/voting/view_results.py - Add reference to blockchain
from database.db_connection import execute_query
from blockchain.secure_results import get_election_results_from_blockchain

def get_all_sessions_with_results():
    """Get all voting sessions with results"""
    query = """
    SELECT vs.*, 
           COUNT(DISTINCT c.id) as candidate_count,
           COUNT(DISTINCT v.id) as vote_count
    FROM voting_sessions vs
    LEFT JOIN candidates c ON vs.id = c.session_id
    LEFT JOIN votes v ON vs.id = v.session_id
    GROUP BY vs.id
    ORDER BY vs.created_at DESC
    """
    sessions = execute_query(query, fetch=True)
    
    results = []
    for session in sessions:
        # Get candidates for this session
        candidates_query = """
        SELECT * FROM candidates 
        WHERE session_id = %s 
        ORDER BY votes DESC, name ASC
        """
        candidates = execute_query(candidates_query, (session['id'],), fetch=True)
        
        # Get blockchain-verified results for comparison
        blockchain_results = get_election_results_from_blockchain(session['id'])
        
        results.append({
            'session': session,
            'candidates': candidates,
            'blockchain_verified': blockchain_results
        })
    
    return results

def view_voting_results():
    """View voting results - UPDATED with blockchain reference"""
    results = get_all_sessions_with_results()
    
    print("\n" + "="*60)
    print("📊 VOTING RESULTS")
    print("="*60)
    print("ℹ️  Note: For blockchain-verified results, use Blockchain Tools")
    print("="*60)
    
    if not results:
        print("No voting sessions created yet.")
        input("\nPress Enter to continue...")
        return
    
    # Display all sessions
    for result in results:
        session = result['session']
        candidates = result['candidates']
        
        print(f"\n🗳️  Session: {session['name']}")
        print(f"   ID: {session['id']}")
        print(f"   Status: {session['status'].upper()}")
        print(f"   Duration: {session.get('duration_minutes', 'N/A')} minutes")
        print(f"   Total Votes (Database): {session['vote_count']}")
        
        if result['blockchain_verified']:
            bc_total = result['blockchain_verified']['total_blockchain_votes']
            if session['vote_count'] == bc_total:
                print(f"   🔒 Blockchain Verified: ✅ MATCH ({bc_total} votes)")
            else:
                print(f"   🔒 Blockchain Verified: ❌ MISMATCH")
                print(f"      Database: {session['vote_count']} votes")
                print(f"      Blockchain: {bc_total} votes")
        
        print(f"   Time: {session.get('start_time', 'N/A')} to {session.get('end_time', 'N/A')}")
        
        if candidates:
            print("\n   👥 Results (from database):")
            print("   " + "-" * 50)
            
            for candidate in candidates:
                votes = candidate['votes']
                total = session['vote_count']
                percentage = (votes / total * 100) if total > 0 else 0
                
                print(f"   {candidate['id']}. {candidate['name']}")
                print(f"     Gender: {candidate.get('gender', 'Not specified')}")
                print(f"     Position: {candidate.get('position', 'Candidate')}")
                print(f"     Votes: {votes} ({percentage:.1f}%)")
                print("   " + "-" * 20)
            
            # Show winner if there are votes
            if session['vote_count'] > 0 and candidates:
                winner = candidates[0]
                winner_percentage = (winner['votes'] / session['vote_count'] * 100) if session['vote_count'] > 0 else 0
                print(f"\n   🏆 Winner: {winner['name']}")
                print(f"     Position: {winner.get('position', 'Candidate')}")
                print(f"     Votes: {winner['votes']} ({winner_percentage:.1f}%)")
        else:
            print("\n   ❌ No candidates in this session")
        
        print("   " + "=" * 50)
    
    print("\n" + "="*60)
    print("💡 Tip: Use 'Blockchain Tools' for tamper-proof verification")
    print("="*60)
    input("\nPress Enter to continue...")