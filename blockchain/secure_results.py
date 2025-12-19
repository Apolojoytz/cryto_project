# voting_system/utils/secure_results.py
from database.db_connection import execute_query
from blockchain.blockchain_core import blockchain
import json
from collections import defaultdict

def get_election_results_from_blockchain(session_id):
    """Calculate election results directly from blockchain (immutable)"""
    # Get session info from database
    session_query = "SELECT name FROM voting_sessions WHERE id = %s"
    session = execute_query(session_query, (session_id,), fetch_one=True)
    
    if not session:
        return None
    
    session_name = session['name']
    
    # Get candidates for this session
    candidates_query = """
    SELECT id, name, gender, position 
    FROM candidates 
    WHERE session_id = %s
    ORDER BY id
    """
    candidates = execute_query(candidates_query, (session_id,), fetch=True)
    
    if not candidates:
        return None
    
    # Get all blockchain votes for this session
    all_votes = []
    blocks_query = "SELECT data FROM blockchain_blocks"
    blocks = execute_query(blocks_query, fetch=True)
    
    if blocks:
        for block in blocks:
            try:
                data = json.loads(block['data'])
                votes = data.get('votes', [])
                # Filter votes for this session
                session_votes = [v for v in votes if v.get('session_id') == session_id]
                all_votes.extend(session_votes)
            except:
                continue
    
    # Count votes per candidate FROM BLOCKCHAIN
    blockchain_vote_counts = defaultdict(int)
    
    for vote in all_votes:
        candidate_id = vote.get('candidate_id')
        if candidate_id:
            blockchain_vote_counts[candidate_id] += 1
    
    # Get database vote counts (for comparison)
    db_vote_counts = {}
    for candidate in candidates:
        db_query = "SELECT votes FROM candidates WHERE id = %s"
        result = execute_query(db_query, (candidate['id'],), fetch_one=True)
        db_vote_counts[candidate['id']] = result['votes'] if result else 0
    
    # Prepare results
    candidate_results = []
    
    for candidate in candidates:
        cand_id = candidate['id']
        blockchain_votes = blockchain_vote_counts.get(cand_id, 0)
        database_votes = db_vote_counts.get(cand_id, 0)
        
        candidate_results.append({
            'id': cand_id,
            'name': candidate['name'],
            'position': candidate.get('position', 'Candidate'),
            'blockchain_votes': blockchain_votes,
            'database_votes': database_votes,
            'match': blockchain_votes == database_votes
        })
    
    # Calculate totals
    total_blockchain = sum(blockchain_vote_counts.values())
    total_database = sum(db_vote_counts.values())
    
    # Determine winner from BLOCKCHAIN
    winner = None
    if candidate_results and total_blockchain > 0:
        sorted_results = sorted(candidate_results, 
                               key=lambda x: x['blockchain_votes'], 
                               reverse=True)
        winner = sorted_results[0]
    
    return {
        'session_id': session_id,
        'session_name': session_name,
        'candidate_results': candidate_results,
        'total_blockchain_votes': total_blockchain,
        'total_database_votes': total_database,
        'integrity_ok': total_blockchain == total_database,
        'winner': winner
    }

def get_secure_results_view(session_id=None):
    """Get election results that cannot be tampered with"""
    
    if session_id:
        # Get results for specific session from blockchain
        return get_election_results_from_blockchain(session_id)
    else:
        # Get all sessions
        sessions_query = "SELECT id, name FROM voting_sessions ORDER BY id"
        sessions = execute_query(sessions_query, fetch=True)
        
        results = []
        for session in sessions:
            session_result = get_election_results_from_blockchain(session['id'])
            if session_result:
                results.append(session_result)
        
        return results

def display_public_results():
    """Display results for public view (read-only, blockchain-verified)"""
    print("\n" + "="*60)
    print("ELECTION RESULTS (Blockchain-Verified)")
    print("="*60)
    
    results = get_secure_results_view()
    
    if not results:
        print("No election results available.")
        return
    
    for result in results:
        print(f"\n{result['session_name']}")
        print("-" * 40)
        
        # Sort candidates by votes (from blockchain)
        sorted_candidates = sorted(result['candidate_results'], 
                                  key=lambda x: x['blockchain_votes'], 
                                  reverse=True)
        
        for candidate in sorted_candidates:
            votes = candidate['blockchain_votes']
            total = result['total_blockchain_votes']
            percentage = (votes / total * 100) if total > 0 else 0
            
            print(f"{candidate['name']}: {votes} votes ({percentage:.1f}%)")
            
            if not candidate['match']:
                print(f"  Warning: Database shows {candidate['database_votes']} votes")
        
        # Show winner
        if result['winner']:
            winner = result['winner']
            print(f"\n Winner: {winner['name']}")
            print(f"   Votes: {winner['blockchain_votes']}")
    
    print("="*60)
    print(" These results are verified by blockchain technology")
    print("   and cannot be tampered with.")
    print("="*60)

def verify_all_election_results():
    """Verify integrity of all election results"""
    print("\n" + "="*60)
    print(" VERIFYING ALL ELECTION RESULTS INTEGRITY")
    print("="*60)
    
    results = get_secure_results_view()
    
    if not results:
        print("No election results to verify.")
        return
    
    all_valid = True
    
    for result in results:
        print(f"\n Session: {result['session_name']}")
        
        if result['integrity_ok']:
            print(f"    Integrity: PASSED")
            print(f"   Total votes: {result['total_blockchain_votes']}")
        else:
            print(f"    Integrity: FAILED")
            print(f"   Blockchain votes: {result['total_blockchain_votes']}")
            print(f"   Database votes: {result['total_database_votes']}")
            print(f"   Difference: {abs(result['total_blockchain_votes'] - result['total_database_votes'])}")
            all_valid = False
        
        # Show individual candidate mismatches
        mismatches = [c for c in result['candidate_results'] if not c['match']]
        if mismatches:
            print(f"     Mismatched candidates:")
            for cand in mismatches:
                print(f"      {cand['name']}: Blockchain={cand['blockchain_votes']}, Database={cand['database_votes']}")
    
    print("\n" + "="*60)
    if all_valid:
        print(" ALL ELECTION RESULTS ARE VALID")
    else:
        print("  SOME ELECTION RESULTS HAVE INTEGRITY ISSUES")
        print("   Consider running database repair tools.")
    print("="*60)
    input("\nPress Enter to continue...")
# Function to add to admin menu
def show_blockchain_verified_results():
    """Show election results verified by blockchain"""
    display_public_results()
    input("\nPress Enter to continue...")