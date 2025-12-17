# voting_system/admin/voting/create_voting.py
from datetime import datetime, timedelta
from database.db_connection import execute_query
from config import ADMIN_EMAIL

# Try to import blockchain
try:
    from blockchain.voting_blockchain import voting_blockchain
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    BLOCKCHAIN_AVAILABLE = False

def create_voting_session():
    """Create a new voting session"""
    print("\n" + "="*40)
    print("🗳️  CREATE VOTING SESSION")
    print("="*40)
    
    # Get session name
    print("\n📝 Voting Details:")
    name = input("Voting Name: ").strip()
    if not name:
        print("❌ Voting name cannot be empty.")
        input("Press Enter to continue...")
        return False
    
    description = input("Description (optional): ").strip()
    if not description:
        description = f"Voting for {name}"
    
    # Add candidates
    print("\n👥 Add Candidates (enter 'done' to finish):")
    print("-" * 40)
    
    candidates = []
    candidate_id = 1
    
    while True:
        print(f"\nCandidate #{candidate_id}:")
        candidate_name = input("  Name: ").strip()
        
        if candidate_name.lower() == 'done':
            if candidate_id == 1:
                print("❌ At least one candidate is required.")
                continue
            else:
                break
        
        if not candidate_name:
            print("❌ Candidate name cannot be empty.")
            continue
        
        # Get gender
        candidate_gender = input("  Gender (Male/Female/Other): ").strip()
        if not candidate_gender:
            candidate_gender = "Not specified"
        
        # Get position
        candidate_position = input("  Position: ").strip()
        if not candidate_position:
            candidate_position = "Candidate"
        
        # Add candidate
        candidates.append({
            'id': candidate_id,
            'name': candidate_name,
            'gender': candidate_gender,
            'position': candidate_position
        })
        
        candidate_id += 1
        
        # Optional: Set a limit if needed
        if candidate_id > 20:  # Maximum 20 candidates
            print("⚠️  Maximum 20 candidates reached.")
            break
    
    if not candidates:
        print("❌ No candidates added. Voting session creation cancelled.")
        input("Press Enter to continue...")
        return False
    
    # Get duration - THIS IS WHERE WE GET duration_minutes
    print("\n⏰ Voting Duration:")
    print("1. 10 minutes")
    print("2. 30 minutes") 
    print("3. 1 hour")
    print("4. 6 hours")
    print("5. 12 hours")
    print("6. 24 hours (1 day)")
    print("7. Custom minutes")
    
    duration_choice = input("\nChoose duration option (1-7): ").strip()
    
    duration_options = {
        '1': 10,      # 10 minutes
        '2': 30,      # 30 minutes
        '3': 60,      # 1 hour
        '4': 360,     # 6 hours
        '5': 720,     # 12 hours
        '6': 1440     # 24 hours
    }
    
    if duration_choice in duration_options:
        duration_minutes = duration_options[duration_choice]  # DEFINE duration_minutes HERE
    elif duration_choice == '7':
        try:
            custom_minutes = int(input("Enter duration in minutes: ").strip())
            if custom_minutes < 10:
                print("⚠️  Minimum duration is 10 minutes. Setting to 10 minutes.")
                duration_minutes = 10
            elif custom_minutes > 1440:
                print("⚠️  Maximum duration is 1440 minutes (24 hours). Setting to 24 hours.")
                duration_minutes = 1440
            else:
                duration_minutes = custom_minutes
        except ValueError:
            print("⚠️  Invalid input. Defaulting to 1 hour.")
            duration_minutes = 60
    else:
        print("⚠️  Invalid choice. Defaulting to 1 hour.")
        duration_minutes = 60
    
    # NOW duration_minutes IS DEFINED! Calculate start and end times
    current_time = datetime.now()
    start_time = current_time
    end_time = current_time + timedelta(minutes=duration_minutes)
    
    # Format dates and times
    start_date_str = start_time.strftime("%Y-%m-%d")
    start_time_str = start_time.strftime("%H:%M")
    end_date_str = end_time.strftime("%Y-%m-%d")
    end_time_str = end_time.strftime("%H:%M")
    
    # Create voting session
    session_query = """
    INSERT INTO voting_sessions (name, description, start_date, start_time, end_date, end_time, duration_minutes, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, 'active')
    """
    session_id = execute_query(session_query, 
        (name, description, start_date_str, start_time_str, end_date_str, end_time_str, duration_minutes),
        lastrowid=True
    )
    
    if not session_id:
        print("❌ Failed to create voting session.")
        input("Press Enter to continue...")
        return False
    
    # Add candidates to database
    for candidate in candidates:
        candidate_query = """
        INSERT INTO candidates (session_id, name, gender, position, votes)
        VALUES (%s, %s, %s, %s, 0)
        """
        execute_query(candidate_query, 
            (session_id, candidate['name'], candidate['gender'], candidate['position'])
        )
    
    # RECORD ON BLOCKCHAIN (if available)
    if BLOCKCHAIN_AVAILABLE and session_id:
        print("\n⛓️  Recording session on blockchain...")
        block_hash = voting_blockchain.record_session_creation(
            session_id, 
            name, 
            ADMIN_EMAIL
        )
        
        if block_hash:
            print("✅ Voting session recorded on blockchain!")
            print(f"📦 Block Hash: {block_hash[:16]}...")
    
    # Display summary
    print("\n" + "="*40)
    print("✅ VOTING SESSION CREATED SUCCESSFULLY!")
    print("="*40)
    print(f"Session ID: {session_id}")
    print(f"Voting Name: {name}")
    print(f"Number of Candidates: {len(candidates)}")
    print(f"Duration: {duration_minutes} minutes ({duration_minutes/60:.1f} hours)")
    print(f"Start Time: {start_time_str}")
    print(f"End Time: {end_time_str}")
    print(f"Status: ACTIVE")
    print("="*40)
    
    # Show candidates summary
    print("\n📋 Candidates List:")
    print("-" * 40)
    for candidate in candidates:
        print(f"{candidate['id']}. {candidate['name']}")
        print(f"   Gender: {candidate['gender']}")
        print(f"   Position: {candidate['position']}")
    
    print("="*40)
    print("\n⚠️  Voting session is now ACTIVE!")
    print("Users can start voting immediately.")
    print("="*40)
    
    input("\nPress Enter to continue...")
    return True