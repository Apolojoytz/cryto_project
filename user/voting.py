import json
import os
import hashlib
from datetime import datetime
from config import DB_FILE, VOTING_SESSIONS_FILE, get_blockchain, save_json, load_json

def get_active_voting_session():
    """Get the currently active voting session"""
    sessions = load_json(VOTING_SESSIONS_FILE)
    
    if not sessions:
        return None
    
    # Check for active sessions
    current_time = datetime.now()
    
    for session in sessions:
        if session['status'] == 'active':
            # Try to parse session dates if available
            try:
                start_str = f"{session['start_date']} {session['start_time']}"
                end_str = f"{session['end_date']} {session['end_time']}"
                start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
                end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
                
                if start_time <= current_time <= end_time:
                    return session
            except:
                # If date parsing fails, just check status
                return session
    
    # If no active session found, check for any session marked as active
    for session in sessions:
        if session['status'] == 'active':
            return session
    
    return None

def vote(email):
    """Handle the voting process with blockchain verification"""
    print("\n" + "="*40)
    print("CAST YOUR VOTE")
    print("="*40)
    
    db = load_json(DB_FILE)
    sessions = load_json(VOTING_SESSIONS_FILE)
    blockchain = get_blockchain()
    
    # Check voting verification
    if not db[email].get('voting_verified', False):
        print("❌ You must complete Voting Verification first!")
        print("Please select option 1 from the User Menu.")
        return False
    
    # Get active voting session
    active_session = get_active_voting_session()
    
    if not active_session:
        print("❌ No active voting session available!")
        print("\n📋 Available Sessions:")
        print("-" * 30)
        
        if not sessions:
            print("No voting sessions created yet.")
        else:
            for session in sessions:
                status_emoji = {
                    "active": "✅",
                    "upcoming": "⏳",
                    "completed": "🏁"
                }.get(session['status'], "❓")
                print(f"{status_emoji} {session['name']} - {session['status'].upper()}")
        
        print("\nPlease wait for the admin to start a voting session.")
        return False
    
    # Check if user has already voted in this session using blockchain
    vote_verification = blockchain.verify_user_vote(email, active_session['id'])
    if vote_verification['verified']:
        print(f"❌ You have already voted in this session!")
        print(f"   Previous vote recorded on blockchain at: {vote_verification.get('timestamp')}")
        print(f"   Voted for: {vote_verification.get('candidate')}")
        print(f"   Block #: {vote_verification.get('block')}")
        print(f"   TX ID: {vote_verification.get('transaction_id')}")
        return False
    
    # Display voting session info
    print(f"\n🗳️  Voting Session: {active_session['name']}")
    print(f"📝 Description: {active_session['description']}")
    
    # Display candidates
    print("\n👥 CANDIDATES:")
    print("-" * 40)
    
    candidates = active_session['candidates']
    for candidate in candidates:
        print(f"{candidate['id']}. {candidate['symbol']} {candidate['name']} - {candidate['party']}")
    
    # Get vote choice
    choice = ""
    valid_choices = [str(c['id']) for c in candidates]
    
    while choice not in valid_choices:
        choice = input(f"\nChoose candidate ({', '.join(valid_choices)}): ").strip()
        if choice not in valid_choices:
            print(f"❌ Please enter a valid candidate number: {', '.join(valid_choices)}")
    
    # Confirm vote
    print("\n" + "-" * 40)
    selected_candidate = next(c for c in candidates if str(c['id']) == choice)
    confirm = input(f"Confirm vote for {selected_candidate['name']} ({selected_candidate['party']})? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Vote cancelled.")
        return False
    
    # Generate unique vote ID
    vote_id = hashlib.sha256(
        f"{email}{active_session['id']}{selected_candidate['id']}{datetime.now().timestamp()}".encode()
    ).hexdigest()[:16]
    
    # Record vote on blockchain FIRST (immutable)
    vote_data = {
        "voter_email": email,
        "voter_username": db[email]['username'],
        "session_id": active_session['id'],
        "session_name": active_session['name'],
        "candidate_id": selected_candidate['id'],
        "candidate_name": selected_candidate['name'],
        "candidate_party": selected_candidate['party'],
        "vote_id": vote_id,
        "timestamp": datetime.now().isoformat()
    }
    
    # Add to blockchain
    block = blockchain.add_transaction("vote", vote_data)
    
    # Update regular database
    # 1. Update session data
    for i, session in enumerate(sessions):
        if session['id'] == active_session['id']:
            # Update candidate votes
            for j, candidate in enumerate(session['candidates']):
                if str(candidate['id']) == choice:
                    sessions[i]['candidates'][j]['votes'] += 1
                    sessions[i]['total_votes'] += 1
                    if 'voters' not in sessions[i]:
                        sessions[i]['voters'] = []
                    sessions[i]['voters'].append(email)
            break
    
    # 2. Update user data
    db[email]['has_voted'] = True
    db[email]['vote_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db[email]['voted_for'] = selected_candidate['name']
    db[email]['voted_session_id'] = active_session['id']
    db[email]['vote_id'] = vote_id
    db[email]['vote_block'] = block.index
    db[email]['vote_transaction_id'] = vote_data.get('transaction_id', '')
    
    # Save all data to regular database
    save_json(VOTING_SESSIONS_FILE, sessions)
    save_json(DB_FILE, db)
    
    print("\n" + "="*40)
    print("✅ YOUR VOTE HAS BEEN RECORDED!")
    print(f"You voted for: {selected_candidate['name']}")
    print(f"Session: {active_session['name']}")
    print(f"Time: {db[email]['vote_time']}")
    print(f"📗 Vote recorded on blockchain Block #{block.index}")
    print(f"🔗 Vote ID: {vote_id}")
    print(f"📊 Total votes in session: {active_session['total_votes'] + 1}")
    print("="*40)
    
    return True