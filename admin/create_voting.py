import json
import hashlib
from datetime import datetime
from config import VOTING_SESSIONS_FILE, get_blockchain, save_json, load_json

def create_voting_session():
    """Create a new voting session with blockchain"""
    print("\n" + "="*50)
    print("CREATE NEW VOTING SESSION")
    print("="*50)
    
    sessions = load_json(VOTING_SESSIONS_FILE)
    blockchain = get_blockchain()
    
    # Get session details
    session_name = input("Session Name: ").strip()
    description = input("Description: ").strip()
    
    # Get candidates
    candidates = []
    print("\nAdd Candidates (enter 'done' when finished):")
    
    candidate_num = 1
    while True:
        name = input(f"\nCandidate {candidate_num} Name (or 'done'): ").strip()
        if name.lower() == 'done':
            if candidate_num < 3:
                print("❌ Minimum 2 candidates required!")
                continue
            break
        
        party = input(f"  Party/Affiliation: ").strip()
        symbol = input(f"  Symbol/Emoji: ").strip()
        
        candidates.append({
            "id": candidate_num,
            "name": name,
            "party": party,
            "symbol": symbol,
            "votes": 0
        })
        candidate_num += 1
    
    # Get voting duration
    print("\nVoting Duration:")
    start_date = input("Start Date (YYYY-MM-DD): ").strip()
    start_time = input("Start Time (HH:MM): ").strip()
    end_date = input("End Date (YYYY-MM-DD): ").strip()
    end_time = input("End Time (HH:MM): ").strip()
    
    # Get session status
    print("\nSession Status:")
    print("1. Active (Users can vote now)")
    print("2. Upcoming (Will start later)")
    print("3. Completed (Voting ended)")
    
    status_choice = input("Choose status (1-3): ").strip()
    status_map = {"1": "active", "2": "upcoming", "3": "completed"}
    status = status_map.get(status_choice, "upcoming")
    
    # Create session
    session_id = len(sessions) + 1
    session_hash = hashlib.sha256(
        f"{session_name}{session_id}{datetime.now().timestamp()}".encode()
    ).hexdigest()[:16]
    
    session = {
        "id": session_id,
        "name": session_name,
        "description": description,
        "candidates": candidates,
        "start_date": start_date,
        "start_time": start_time,
        "end_date": end_date,
        "end_time": end_time,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "total_votes": 0,
        "voters": [],
        "session_hash": session_hash
    }
    
    sessions.append(session)
    save_json(VOTING_SESSIONS_FILE, sessions)
    
    # Record session creation on blockchain
    session_data = {
        "session_id": session_id,
        "session_name": session_name,
        "candidates": [c['name'] for c in candidates],
        "status": status,
        "session_hash": session_hash,
        "timestamp": datetime.now().isoformat()
    }
    
    blockchain.add_transaction("session_creation", session_data)
    
    print(f"\n✅ Voting session created successfully!")
    print(f"   📋 Session ID: {session_id}")
    print(f"   📝 Name: {session_name}")
    print(f"   👥 Candidates: {len(candidates)}")
    print(f"   🗳️  Status: {status.upper()}")
    print(f"   📅 Period: {start_date} {start_time} to {end_date} {end_time}")
    print(f"   📗 Transaction recorded on blockchain")
    print(f"   🔗 Session Hash: {session_hash}")

def view_voting_sessions():
    """View all voting sessions"""
    sessions = load_json(VOTING_SESSIONS_FILE)
    
    print("\n" + "="*80)
    print("VOTING SESSIONS")
    print("="*80)
    
    if not sessions:
        print("No voting sessions found.")
        return
    
    for session in sessions:
        status_emoji = {
            "active": "✅",
            "upcoming": "⏳",
            "completed": "🏁"
        }.get(session['status'], "❓")
        
        print(f"\n{status_emoji} Session #{session['id']}: {session['name']}")
        print(f"   Description: {session['description']}")
        print(f"   Status: {session['status'].upper()}")
        print(f"   Created: {session['created_at']}")
        print(f"   Period: {session['start_date']} {session['start_time']} to {session['end_date']} {session['end_time']}")
        print(f"   Candidates: {len(session['candidates'])} | Total Votes: {session['total_votes']}")
        print(f"   Hash: {session.get('session_hash', 'N/A')[:16]}...")
        
        print("   Candidates:")
        for candidate in session['candidates']:
            print(f"     {candidate['id']}. {candidate['symbol']} {candidate['name']} ({candidate['party']}) - Votes: {candidate['votes']}")
    
    print("="*80)
    input("\nPress Enter to continue...")