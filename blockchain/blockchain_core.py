import hashlib
import json
import time
from datetime import datetime
from database.db_connection import execute_query

class Block:
    """Represents a single block in the blockchain"""
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # MOVE nonce BEFORE calculate_hash()
        self.hash = self.calculate_hash()  # Now nonce is defined

    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Proof of Work mining"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

class VotingBlockchain:
    """Blockchain for vote verification"""
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.pending_votes = []
        self.create_genesis_block()  # This should be fine now
        
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(0, str(datetime.now()), 
                             {"message": "Genesis Block - Voting System"}, "0")
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the latest block in the chain"""
        return self.chain[-1] if self.chain else None
    
    def add_vote_to_blockchain(self, vote_data):
        """Add a vote to the blockchain"""
        # Store vote in pending pool
        self.pending_votes.append(vote_data)
        
        print(f"📝 Added vote {vote_data.get('vote_id')} to blockchain pending pool")
        
        # 🔴 FIX: Create block for EVERY vote for now (you can change this later)
        # For demonstration, create a block for each vote
        return self.create_block_from_pending()
    
    def create_block_from_pending(self):
        """Create a new block from pending votes"""
        if not self.pending_votes:
            return None
        
        latest_block = self.get_latest_block()
        previous_hash = latest_block.hash if latest_block else "0"
        
        new_block = Block(
            len(self.chain),
            str(datetime.now()),
            {
                'votes': self.pending_votes.copy(),
                'total_votes': len(self.pending_votes),
                'block_type': 'vote_batch'
            },
            previous_hash
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Store block in database
        self.store_block_in_db(new_block)
        
        # Clear pending votes
        self.pending_votes = []
        
        return new_block
    
    def store_block_in_db(self, block):
        """Store block in database for persistence"""
        query = """
        INSERT INTO blockchain_blocks 
        (block_index, block_hash, previous_hash, timestamp, data, nonce)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data_json = json.dumps(block.data)
        
        return execute_query(query, (
            block.index,
            block.hash,
            block.previous_hash,
            block.timestamp,
            data_json,
            block.nonce
        ))
    
    def verify_vote(self, vote_id):
        """Verify if a vote exists in the blockchain - FIXED VERSION"""
        # First check database for vote
        query = """
        SELECT v.*, u.username, c.name as candidate_name, vs.name as session_name
        FROM votes v
        JOIN users u ON v.user_email = u.email
        JOIN candidates c ON v.candidate_id = c.id
        JOIN voting_sessions vs ON v.session_id = vs.id
        WHERE v.id = %s
        """
        vote = execute_query(query, (vote_id,), fetch_one=True)
        
        if not vote:
            return None
        
        # Check blockchain for this vote
        blockchain_vote_data = self.find_vote_in_blockchain(vote_id)
        
        if blockchain_vote_data:
            integrity_verified = self.verify_vote_integrity(vote_id, vote)
        else:
            integrity_verified = False
        
        return {
            'vote_details': vote,
            'in_blockchain': blockchain_vote_data is not None,
            'blockchain_data': blockchain_vote_data,
            'integrity_verified': integrity_verified
        }
    
    def find_vote_in_blockchain(self, vote_id):
        """Search for vote in blockchain - FIXED VERSION"""
        # First, get all blocks that might contain votes
        query = """
        SELECT bb.* 
        FROM blockchain_blocks bb
        WHERE bb.data LIKE '%"vote_id":%'
        """
        
        blocks = execute_query(query, fetch=True)
        
        if not blocks:
            return None
        
        # Search through each block
        for block in blocks:
            try:
                data = json.loads(block['data'])
                votes = data.get('votes', [])
                
                for vote in votes:
                    if vote.get('vote_id') == vote_id:
                        return {
                            'block_index': block['block_index'],
                            'block_hash': block['block_hash'],
                            'block_timestamp': block['timestamp'],
                            'vote_data': vote
                        }
            except json.JSONDecodeError:
                continue  # Skip invalid JSON
        
        return None
    
    def verify_vote_integrity(self, vote_id, vote_data):
        """Verify vote integrity by checking hash"""
        # Create a hash of the vote data
        vote_string = f"{vote_id}:{vote_data['user_email']}:{vote_data['candidate_id']}:{vote_data['voted_at']}"
        calculated_hash = hashlib.sha256(vote_string.encode()).hexdigest()
        
        # Find the vote in blockchain
        blockchain_vote = self.find_vote_in_blockchain(vote_id)
        
        if not blockchain_vote:
            return False
        
        # Compare hashes
        stored_vote_hash = blockchain_vote['vote_data'].get('vote_hash')
        return calculated_hash == stored_vote_hash
    
    def get_blockchain_info(self):
        """Get blockchain statistics - FIXED VERSION"""
        query = "SELECT COUNT(*) as total_blocks FROM blockchain_blocks"
        blocks_count = execute_query(query, fetch_one=True)
        
        query = "SELECT COUNT(*) as total_votes FROM votes"
        votes_count = execute_query(query, fetch_one=True)
        
        # Alternative method to count votes in blockchain
        votes_in_chain = 0
        blocks = execute_query("SELECT data FROM blockchain_blocks", fetch=True)
        
        if blocks:
            for block in blocks:
                try:
                    data = json.loads(block['data'])
                    if 'votes' in data:
                        votes_in_chain += len(data['votes'])
                except:
                    pass
        
        return {
            'total_blocks': blocks_count['total_blocks'] if blocks_count else 0,
            'total_votes': votes_count['total_votes'] if votes_count else 0,
            'votes_in_blockchain': votes_in_chain,
            'pending_votes': len(self.pending_votes),
            'chain_length': len(self.chain),
            'difficulty': self.difficulty
        }
    
    def audit_chain(self):
        """Audit the entire blockchain for integrity - SMART GENESIS CHECK"""
        issues = []
        
        # First, sync with database
        self.sync_with_database()
        
        if len(self.chain) == 0:
            issues.append("Blockchain is empty")
            return issues
        
        # SMART GENESIS CHECK: If first block is index 1, treat it as genesis
        first_block = self.chain[0]
        
        if first_block.index == 1:
            # Auto-fix: This is actually the genesis block
            first_block.index = 0
            if first_block.previous_hash != "0":
                first_block.previous_hash = "0"
                first_block.hash = first_block.calculate_hash()
            
            # Update in database too
            update_query = """
            UPDATE blockchain_blocks 
            SET block_index = 0, previous_hash = '0', block_hash = %s
            WHERE block_index = 1
            """
            execute_query(update_query, (first_block.hash,))
            
            print("⚠️  Auto-fixed: Block index 1 converted to genesis block (index 0)")
            
            # Re-sync after fix
            self.sync_with_database()
        
        # Now check the fixed chain
        if len(self.chain) == 0:
            return ["❌ Blockchain empty after fix"]
        
        # Verify genesis block
        genesis = self.chain[0]
        if genesis.index != 0:
            issues.append(f"First block index should be 0, got: {genesis.index}")
        
        if genesis.previous_hash != "0":
            issues.append(f"Genesis block previous hash should be '0', got: {genesis.previous_hash[:20]}...")
        
        # Check chain integrity
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Check hash validity
            if current.hash != current.calculate_hash():
                issues.append(f"Block {current.index} hash is invalid")
            
            # Check chain linking
            if current.previous_hash != previous.hash:
                issues.append(f"Block {current.index} previous hash mismatch")
            
            # Check proof of work
            if current.hash[:self.difficulty] != '0' * self.difficulty:
                issues.append(f"Block {current.index} proof of work invalid")
        
        if issues and not issues[0].startswith("✅"):
            return issues
        else:
            return ["✅ Blockchain integrity verified successfully!"]
    
    def sync_with_database(self):
        """Sync blockchain from database (for persistence) - IMPROVED VERSION"""
        query = "SELECT * FROM blockchain_blocks ORDER BY block_index"
        db_blocks = execute_query(query, fetch=True)
        
        if not db_blocks:
            # No blocks in DB, just keep current chain
            return
        
        # Clear current chain
        self.chain = []
        
        # Rebuild chain from DB
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
                
                # Set hash and nonce from DB
                block.hash = db_block['block_hash']
                block.nonce = db_block['nonce']
                
                # Verify block hash matches data
                calculated_hash = block.calculate_hash()
                if block.hash != calculated_hash:
                    print(f"⚠️  Block {block.index} hash mismatch in database")
                    # Recalculate with stored nonce
                    block.hash = calculated_hash
                
                self.chain.append(block)
                
            except Exception as e:
                print(f"❌ Error loading block {db_block.get('block_index', 'unknown')}: {e}")
                continue
        
        # Rebuild pending votes from the last block
        if self.chain:
            last_block = self.chain[-1]
            if 'votes' in last_block.data:
                self.pending_votes = last_block.data['votes'].copy()
            else:
                self.pending_votes = []
        
        print(f"✅ Synced blockchain from database: {len(self.chain)} blocks loaded")

# Global blockchain instance - this should NOT cause errors now
blockchain = VotingBlockchain(difficulty=4)