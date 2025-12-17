# voting_system/blockchain/repair_tools.py
from .blockchain_core import blockchain, Block
import json
from database.db_connection import execute_query

def repair_blockchain():
    """Repair blockchain inconsistencies"""
    print("\n" + "="*50)
    print("🔧 BLOCKCHAIN REPAIR TOOL")
    print("="*50)
    
    print("1. Checking blockchain integrity...")
    issues = blockchain.audit_chain()
    
    if not issues or issues[0] == "✅ Blockchain integrity verified successfully!":
        print("✅ Blockchain is already healthy!")
        input("Press Enter to continue...")
        return
    
    print(f"❌ Found {len(issues)} issues")
    
    print("\n2. Attempting to repair...")
    
    # Strategy 1: Rebuild chain from database
    print("   Rebuilding chain from database...")
    
    # Get all blocks from database
    query = "SELECT * FROM blockchain_blocks ORDER BY block_index"
    db_blocks = execute_query(query, fetch=True)
    
    if not db_blocks:
        print("   ❌ No blocks in database to rebuild from")
        input("Press Enter to continue...")
        return
    
    # Clear and rebuild
    blockchain.chain = []
    
    for db_block in db_blocks:
        try:
            block_data = json.loads(db_block['data'])
            
            # Create block
            block = Block(
                db_block['block_index'],
                db_block['timestamp'],
                block_data,
                db_block['previous_hash']
            )
            
            # Set properties
            block.hash = db_block['block_hash']
            block.nonce = db_block['nonce']
            
            blockchain.chain.append(block)
            
        except Exception as e:
            print(f"   ❌ Error loading block {db_block['block_index']}: {e}")
            continue
    
    print(f"   ✅ Rebuilt chain with {len(blockchain.chain)} blocks")
    
    # Strategy 2: Fix linking
    print("\n   Fixing block linking...")
    for i in range(1, len(blockchain.chain)):
        current = blockchain.chain[i]
        previous = blockchain.chain[i-1]
        
        if current.previous_hash != previous.hash:
            print(f"   Fixing Block #{current.index} previous hash...")
            current.previous_hash = previous.hash
            
            # Recalculate hash
            current.hash = current.calculate_hash()
            
            # Update in database
            update_query = """
            UPDATE blockchain_blocks 
            SET previous_hash = %s, block_hash = %s
            WHERE block_index = %s
            """
            execute_query(update_query, (previous.hash, current.hash, current.index))
    
    print("   ✅ Block linking repaired")
    
    # Strategy 3: Re-verify votes
    print("\n   Re-verifying votes in blockchain...")
    query = "SELECT id FROM votes"
    votes = execute_query(query, fetch=True)
    
    verified_count = 0
    for vote in votes:
        result = blockchain.verify_vote(vote['id'])
        if result and result['in_blockchain']:
            verified_count += 1
    
    print(f"   ✅ {verified_count} votes verified in blockchain")
    
    print("\n3. Final integrity check...")
    final_issues = blockchain.audit_chain()
    
    if not final_issues or final_issues[0] == "✅ Blockchain integrity verified successfully!":
        print("✅ Blockchain repair successful!")
    else:
        print("⚠️  Some issues remain:")
        for issue in final_issues[:5]:  # Show first 5 issues only
            print(f"   • {issue}")
    
    print("="*50)
    input("Press Enter to continue...")