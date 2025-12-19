# voting_system/utils/blockchain_repair.py
from database.db_connection import execute_query

def fix_database_votes_from_blockchain():
    """Fix database vote counts to match blockchain"""
    print("\n" + "="*60)
    print("REPAIRING DATABASE VOTE COUNTS")
    print("="*60)
    
    # Get all sessions
    sessions_query = "SELECT id FROM voting_sessions"
    sessions = execute_query(sessions_query, fetch=True)
    
    if not sessions:
        print("No voting sessions found.")
        return
    
    fixed_count = 0
    
    for session in sessions:
        session_id = session['id']
        
        # Get blockchain results for this session
        from blockchain.secure_results import get_election_results_from_blockchain
        result = get_election_results_from_blockchain(session_id)
        
        if not result or result['integrity_ok']:
            continue  # No mismatch or can't get results
        
        # Fix each candidate
        for candidate in result['candidate_results']:
            cand_id = candidate['id']
            blockchain_votes = candidate['blockchain_votes']
            database_votes = candidate['database_votes']
            
            if blockchain_votes != database_votes:
                # Update database to match blockchain
                update_query = "UPDATE candidates SET votes = %s WHERE id = %s"
                execute_query(update_query, (blockchain_votes, cand_id))
                fixed_count += 1
                
                print(f"Fixed candidate {candidate['name']}: {database_votes} → {blockchain_votes}")
    
    print(f"\n✅ Fixed {fixed_count} candidate vote counts")
    print("="*60)
    input("Press Enter to continue...")