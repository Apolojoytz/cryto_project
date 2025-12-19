from database.db_connection import execute_query

def get_database_statistics():
    """Get comprehensive database statistics"""
    stats = {}
    
    # Counts for each table
    tables = ['users', 'voting_verification', 'voting_sessions', 'candidates', 'votes', 'otp_codes', 'blockchain_blocks']
    
    for table in tables:
        query = f"SELECT COUNT(*) as count FROM {table}"
        result = execute_query(query, fetch_one=True)
        stats[f'{table}_count'] = result['count'] if result else 0
    
    # Additional stats
    stats['verified_users'] = execute_query(
        "SELECT COUNT(*) as count FROM users WHERE email_verified = TRUE", 
        fetch_one=True
    )['count']
    
    stats['voting_verified_users'] = execute_query(
        "SELECT COUNT(*) as count FROM users WHERE voting_verified = TRUE", 
        fetch_one=True
    )['count']
    
    stats['users_voted'] = execute_query(
        "SELECT COUNT(*) as count FROM users WHERE has_voted = TRUE", 
        fetch_one=True
    )['count']
    
    stats['active_sessions'] = execute_query(
        "SELECT COUNT(*) as count FROM voting_sessions WHERE status = 'active'", 
        fetch_one=True
    )['count']
    
    return stats

def view_database_statistics():
    """View database statistics"""
    stats = get_database_statistics()
    
    print("\n" + "="*50)
    print("📊 DATABASE STATISTICS")
    print("="*50)
    
    print("\n👥 USER STATISTICS:")
    print(f"   Total Users: {stats['users_count']}")
    print(f"   Email Verified: {stats['verified_users']}")
    print(f"   Voting Verified: {stats['voting_verified_users']}")
    print(f"   Users Who Voted: {stats['users_voted']}")
    
    print("\n🗳️  VOTING STATISTICS:")
    print(f"   Voting Sessions: {stats['voting_sessions_count']}")
    print(f"   Active Sessions: {stats['active_sessions']}")
    print(f"   Candidates: {stats['candidates_count']}")
    print(f"   Total Votes: {stats['votes_count']}")
    
    print("\n⛓️  BLOCKCHAIN STATISTICS:")
    print(f"   Blocks in Chain: {stats['blockchain_blocks_count']}")
    print(f"   Blockchain Coverage: {(stats['votes_count'] - stats['blockchain_blocks_count'] * 10) if stats['votes_count'] > 0 else 0} votes pending")
    
    print("="*50)
    input("\nPress Enter to continue...")