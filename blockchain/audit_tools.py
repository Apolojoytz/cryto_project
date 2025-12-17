from .blockchain_core import blockchain
import json

def view_blockchain_info():
    """Display blockchain information"""
    print("\n" + "="*50)
    print("⛓️  BLOCKCHAIN INFORMATION")
    print("="*50)
    
    info = blockchain.get_blockchain_info()
    
    print(f"\n📊 STATISTICS:")
    print(f"   Total Blocks: {info['total_blocks']}")
    print(f"   Chain Length: {info['chain_length']}")
    print(f"   Mining Difficulty: {info['difficulty']}")
    print(f"   Pending Votes: {info['pending_votes']}")
    
    print(f"\n🗳️  VOTE STATISTICS:")
    print(f"   Total Votes in Database: {info['total_votes']}")
    print(f"   Votes in Blockchain: {info['votes_in_blockchain']}")
    
    if info['total_votes'] > 0:
        percentage = (info['votes_in_blockchain'] / info['total_votes']) * 100
        print(f"   Blockchain Coverage: {percentage:.1f}%")
    
    print(f"\n🔗 LATEST BLOCK:")
    if blockchain.chain:
        latest = blockchain.get_latest_block()
        print(f"   Block #{latest.index}")
        print(f"   Hash: {latest.hash[:30]}...")
        print(f"   Timestamp: {latest.timestamp}")
        print(f"   Votes in Block: {len(latest.data.get('votes', []))}")
    
    print("="*50)
    input("\nPress Enter to continue...")

def audit_blockchain():
    """Perform blockchain audit"""
    print("\n" + "="*50)
    print("🔒 BLOCKCHAIN AUDIT")
    print("="*50)
    
    print("\n⏳ Running blockchain integrity check...")
    
    # Sync with database first
    blockchain.sync_with_database()
    
    # Perform audit
    issues = blockchain.audit_chain()
    
    if issues and issues[0] != "Blockchain integrity verified successfully":
        print("\n❌ ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ Blockchain integrity verified successfully!")
        
        # Show chain structure
        if blockchain.chain:
            print(f"\n📏 CHAIN STRUCTURE:")
            for block in blockchain.chain:
                status = "✓" if block.index == 0 else "⛓️"
                print(f"   {status} Block #{block.index} [{block.hash[:20]}...]")
                if block.data.get('votes'):
                    print(f"      Contains {len(block.data['votes'])} votes")
    
    print("="*50)
    input("\nPress Enter to continue...")