# voting_system/user/voting/voting.py
from datetime import datetime
from database.db_connection import execute_query

# Try to import blockchain
try:
    from blockchain.voting_blockchain import voting_blockchain
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    BLOCKCHAIN_AVAILABLE = False
    print("⚠️  Blockchain module not available")

def get_user_by_email(email):
    """Get user by email"""
    query = """
    SELECT u.*, vv.fullname, vv.gender, vv.phone 
    FROM users u
    LEFT JOIN voting_verification vv ON u.email = vv.user_email
    WHERE u.email = %s
    """
    return execute_query(query, (email,), fetch_one=True)

def get_active_voting_session():
    """Get active voting session with candidates"""
    # First get active session
    session_query = """
    SELECT * FROM voting_sessions 
    WHERE status = 'active' 
      AND CONCAT(end_date, ' ', end_time) > NOW()
    ORDER BY created_at DESC 
    LIMIT 1
    """
    session = execute_query(session_query, fetch_one=True)
    
    if not session:
        return None
    
    # Get candidates for this session
    candidates_query = """
    SELECT * FROM candidates 
    WHERE session_id = %s 
    ORDER BY id
    """
    candidates = execute_query(candidates_query, (session['id'],), fetch=True)
    
    if candidates:
        session['candidates'] = candidates
    
    return session

def check_user_voted(session_id, email):
    """Check if user has already voted in this session"""
    query = "SELECT id FROM votes WHERE session_id = %s AND user_email = %s"
    return execute_query(query, (session_id, email), fetch_one=True) is not None

def cast_vote(session_id, email, candidate_id, candidate_name):
    """Cast a vote in database"""
    # Insert vote
    vote_query = """
    INSERT INTO votes (session_id, user_email, candidate_id)
    VALUES (%s, %s, %s)
    """
    vote_result = execute_query(vote_query, (session_id, email, candidate_id), lastrowid=True)
    
    if not vote_result:
        return False
    
    # Update candidate votes
    update_candidate = "UPDATE candidates SET votes = votes + 1 WHERE id = %s"
    execute_query(update_candidate, (candidate_id,))
    
    # Update session total votes
    update_session = "UPDATE voting_sessions SET total_votes = total_votes + 1 WHERE id = %s"
    execute_query(update_session, (session_id,))
    
    # Update user vote status
    update_user = """
    UPDATE users 
    SET has_voted = TRUE, voted_for = %s, voted_session_id = %s, vote_time = NOW()
    WHERE email = %s
    """
    execute_query(update_user, (candidate_name, session_id, email))
    
    return True

def vote(email):
    """Handle the voting process with blockchain recording"""
    print("\n" + "="*40)
    print("CAST YOUR VOTE")
    print("="*40)
    
    user = get_user_by_email(email)
    
    if not user:
        print("❌ User not found!")
        input("Press Enter to continue...")
        return False
    
    # Check voting verification
    if not user.get('voting_verified', False):
        print("❌ You must complete Voting Verification first!")
        print("Please select option 1 from the User Dashboard.")
        input("Press Enter to continue...")
        return False
    
    # Get active voting session
    active_session = get_active_voting_session()
    
    if not active_session:
        print("❌ No active voting session available!")
        print("Please wait for the admin to start a voting session.")
        input("Press Enter to continue...")
        return False
    
    # Check if user has already voted in this session
    if check_user_voted(active_session['id'], email):
        print("❌ You have already voted in this session!")
        input("Press Enter to continue...")
        return False
    
    # Display voting session info
    print(f"\n🗳️  Voting Session: {active_session['name']}")
    if active_session.get('description'):
        print(f"📝 Description: {active_session['description']}")
    
    # Display candidates
    if not active_session.get('candidates'):
        print("❌ No candidates available for this session.")
        input("Press Enter to continue...")
        return False
    
    print("\n👥 CANDIDATES:")
    print("-" * 40)
    
    candidates = active_session['candidates']
    for candidate in candidates:
        print(f"{candidate['id']}. {candidate['name']}")
        print(f"   Gender: {candidate.get('gender', 'Not specified')}")
        print(f"   Position: {candidate.get('position', 'Candidate')}")
        print()
    
    # Get vote choice
    choice = ""
    valid_choices = [str(c['id']) for c in candidates]
    
    while choice not in valid_choices:
        choice = input(f"Choose candidate ({', '.join(valid_choices)}): ").strip()
        if choice not in valid_choices:
            print(f"❌ Please enter a valid candidate number: {', '.join(valid_choices)}")

    # Get selected candidate
    selected_candidate = None
    for candidate in candidates:
        if str(candidate['id']) == choice:
            selected_candidate = candidate
            break
    
    if not selected_candidate:
        print("❌ Candidate not found!")
        input("Press Enter to continue...")
        return False
    
    # Confirm vote
    print("\n" + "-" * 40)
    confirm = input(f"Confirm vote for {selected_candidate['name']}? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Vote cancelled.")
        input("Press Enter to continue...")
        return False
    
    # Cast the vote in database
    if cast_vote(active_session['id'], email, selected_candidate['id'], selected_candidate['name']):
        # ✅✅✅ CRITICAL: RECORD ON BLOCKCHAIN ✅✅✅
        if BLOCKCHAIN_AVAILABLE:
            print("\n⛓️  Recording vote on blockchain...")
            try:
                block_hash = voting_blockchain.record_vote(
                    active_session['id'],
                    email,
                    selected_candidate['id'],
                    selected_candidate['name']
                )
                
                if block_hash:
                    print("✅ Vote recorded on blockchain!")
                    print(f"📦 Block Hash: {block_hash[:16]}...")
                    
                    # Also show in blockchain audit
                    print(f"📝 Added to block #{len(voting_blockchain.blockchain.chain)-1}")
                else:
                    print("⚠️  Vote recorded in database but blockchain recording failed")
            except Exception as e:
                print(f"⚠️  Blockchain error: {e}")
                print("   Vote saved to database but not to blockchain")
        else:
            print("⚠️  Blockchain not available - vote saved to database only")
        
        print("\n" + "="*40)
        print("✅ YOUR VOTE HAS BEEN RECORDED!")
        print(f"You voted for: {selected_candidate['name']}")
        print(f"Session: {active_session['name']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*40)
    else:
        print("❌ Failed to record your vote. Please try again.")
    
    input("Press Enter to continue...")
    return True