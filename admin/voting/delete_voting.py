# voting_system/admin/voting/delete_voting.py
from database.db_connection import execute_query

def get_all_sessions():
    """Get all voting sessions"""
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
    return execute_query(query, fetch=True)

def get_session_details(session_id):
    """Get session details"""
    query = """
    SELECT vs.*, 
           COUNT(DISTINCT c.id) as candidate_count,
           COUNT(DISTINCT v.id) as vote_count,
           GROUP_CONCAT(CONCAT(c.name, ' (', COALESCE(c.position, 'Candidate'), ')')) as candidates
    FROM voting_sessions vs
    LEFT JOIN candidates c ON vs.id = c.session_id
    LEFT JOIN votes v ON vs.id = v.session_id
    WHERE vs.id = %s
    GROUP BY vs.id
    """
    return execute_query(query, (session_id,), fetch_one=True)

def delete_voting_session():
    """Delete a voting session"""
    print("\n" + "="*40)
    print("🗑️  DELETE VOTING SESSION")
    print("="*40)
    
    sessions = get_all_sessions()
    
    if not sessions:
        print("❌ No voting sessions available to delete.")
        input("Press Enter to continue...")
        return False
    
    # Display available sessions
    print("\n📋 Available Voting Sessions:")
    print("-" * 50)
    for session in sessions:
        status_emoji = {
            "active": "✅",
            "upcoming": "⏳",
            "completed": "🏁"
        }.get(session['status'], "❓")
        
        print(f"{session['id']}. {session['name']}")
        print(f"   Status: {status_emoji} {session['status'].upper()}")
        print(f"   Duration: {session.get('duration_minutes', 'N/A')} minutes")
        print(f"   Candidates: {session['candidate_count']}")
        print(f"   Votes: {session['vote_count']}")
        print(f"   Created: {session['created_at']}")
        print()
    
    # Get session to delete
    try:
        session_id = int(input("Enter Session ID to delete (0 to cancel): ").strip())
    except ValueError:
        print("❌ Invalid session ID.")
        input("Press Enter to continue...")
        return False
    
    if session_id == 0:
        print("❌ Deletion cancelled.")
        input("Press Enter to continue...")
        return False
    
    # Get session details
    session_details = get_session_details(session_id)
    if not session_details:
        print("❌ Session not found.")
        input("Press Enter to continue...")
        return False
    
    print(f"\n⚠️  WARNING: You are about to delete:")
    print(f"   Session: {session_details['name']}")
    print(f"   Status: {session_details['status']}")
    print(f"   Candidates: {session_details['candidate_count']}")
    print(f"   Total Votes: {session_details['vote_count']}")
    
    if session_details.get('candidates'):
        print(f"   Candidate List: {session_details['candidates']}")
    
    confirm = input("\nAre you sure you want to delete this session? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Deletion cancelled.")
        input("Press Enter to continue...")
        return False
    
    # Delete the session (cascade will delete candidates and votes)
    delete_query = "DELETE FROM voting_sessions WHERE id = %s"
    result = execute_query(delete_query, (session_id,))
    
    if result:
        print("\n✅ Voting session deleted successfully!")
    else:
        print("\n❌ Failed to delete voting session.")
    
    input("Press Enter to continue...")
    return result