# voting_system/blockchain/blockchain.py
import hashlib
import json
import os
from datetime import datetime
from config import DB_PATH

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine the block with given difficulty"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_data = {
            "message": "Genesis Block - Voting System Blockchain",
            "created_at": str(datetime.now())
        }
        genesis_block = Block(0, str(datetime.now()), genesis_data, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain"""
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=str(datetime.now()),
            data=data,
            previous_hash=latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check if block is properly mined
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False
        
        return True
    
    def to_dict(self):
        """Convert blockchain to dictionary"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty,
            "length": len(self.chain),
            "is_valid": self.is_chain_valid()
        }
    
    def save_to_file(self, filename=None):
        """Save blockchain to JSON file"""
        if filename is None:
            blockchain_dir = os.path.join(os.path.dirname(DB_PATH), 'blockchain')
            os.makedirs(blockchain_dir, exist_ok=True)
            filename = os.path.join(blockchain_dir, 'blockchain.json')
        
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4, default=str)
    
    def load_from_file(self, filename=None):
        """Load blockchain from JSON file"""
        if filename is None:
            blockchain_dir = os.path.join(os.path.dirname(DB_PATH), 'blockchain')
            filename = os.path.join(blockchain_dir, 'blockchain.json')
        
        if not os.path.exists(filename):
            return False
        
        with open(filename, 'r') as f:
            data = json.load(f)
            
            # Reconstruct blockchain
            self.chain = []
            for block_data in data['chain']:
                block = Block(
                    index=block_data['index'],
                    timestamp=block_data['timestamp'],
                    data=block_data['data'],
                    previous_hash=block_data['previous_hash']
                )
                block.nonce = block_data['nonce']
                block.hash = block_data['hash']
                self.chain.append(block)
            
            self.difficulty = data['difficulty']
        
        return True

# Singleton instance
blockchain_instance = Blockchain()