import json
import os
import hashlib
from datetime import datetime
from .block import Block

class VotingBlockchain:
    def __init__(self, ledger_file="ledger.json"):
        """
        Initialize the blockchain for voting system.
        
        Args:
            ledger_file: Path to store blockchain ledger
        """
        self.chain = []
        self.difficulty = 3  # Lower difficulty for faster processing
        self.ledger_file = ledger_file
        
        # Load existing blockchain or create genesis block
        self.load_chain()
        
        if len(self.chain) == 0:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_data = {
            "type": "genesis",
            "message": "Online Voting System Blockchain Initialized",
            "timestamp": datetime.now().isoformat(),
            "system": "Secure Voting System v1.0"
        }
        
        genesis_block = Block(0, datetime.now().isoformat(), 
                            genesis_data, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_chain()
        print("✅ Genesis block created")
    
    def get_latest_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1] if self.chain else None
    
    def add_transaction(self, transaction_type, transaction_data):
        """
        Add a new transaction to the blockchain.
        
        Args:
            transaction_type: Type of transaction (vote, registration, verification, etc.)
            transaction_data: Data associated with the transaction
        """
        # Create transaction with metadata
        transaction = {
            "type": transaction_type,
            "data": transaction_data,
            "timestamp": datetime.now().isoformat(),
            "transaction_id": self.generate_transaction_id(transaction_data)
        }
        
        # Create new block
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=transaction,
            previous_hash=previous_block.hash if previous_block else "0"
        )
        
        # Mine the block
        print(f"⛏️  Mining block #{len(self.chain)}...")
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Save to file
        self.save_chain()
        
        print(f"✅ Block #{new_block.index} mined successfully!")
        print(f"   Hash: {new_block.hash[:16]}...")
        print(f"   Transaction: {transaction_type}")
        
        return new_block
    
    def generate_transaction_id(self, data):
        """Generate unique transaction ID"""
        import json
        data_string = json.dumps(data, sort_keys=True) + str(datetime.now().timestamp())
        return hashlib.sha256(data_string.encode()).hexdigest()[:16]
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
            
            # Check proof of work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Invalid proof of work at block {i}")
                return False
        
        return True
    
    def save_chain(self):
        """Save blockchain to file"""
        chain_data = [block.to_dict() for block in self.chain]
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        
        with open(self.ledger_file, 'w') as f:
            json.dump(chain_data, f, indent=2)
    
    def load_chain(self):
        """Load blockchain from file"""
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, 'r') as f:
                    chain_data = json.load(f)
                
                self.chain = []
                for block_data in chain_data:
                    block = Block(
                        index=block_data['index'],
                        timestamp=block_data['timestamp'],
                        data=block_data['data'],
                        previous_hash=block_data['previous_hash'],
                        nonce=block_data['nonce']
                    )
                    block.hash = block_data['hash']
                    self.chain.append(block)
                
                # Validate loaded chain
                if not self.is_chain_valid():
                    print("⚠️  Warning: Loaded blockchain is invalid!")
                    self.chain = []
                else:
                    print(f"✅ Loaded {len(self.chain)} blocks from blockchain")
            
            except Exception as e:
                print(f"❌ Error loading blockchain: {e}")
                self.chain = []
    
    def get_transactions_by_type(self, transaction_type):
        """Get all transactions of a specific type"""
        transactions = []
        
        for block in self.chain:
            if block.index == 0:  # Skip genesis block
                continue
            
            transaction = block.data
            if transaction.get('type') == transaction_type:
                transactions.append({
                    "block": block.index,
                    "timestamp": transaction.get('timestamp'),
                    "data": transaction.get('data'),
                    "transaction_id": transaction.get('transaction_id')
                })
        
        return transactions
    
    def get_user_transactions(self, email):
        """Get all transactions for a specific user"""
        transactions = []
        
        for block in self.chain:
            if block.index == 0:
                continue
            
            transaction = block.data
            data = transaction.get('data', {})
            
            # Check if this transaction involves the user
            if (data.get('email') == email or 
                data.get('voter_email') == email or
                data.get('user_email') == email):
                transactions.append({
                    "block": block.index,
                    "type": transaction.get('type'),
                    "timestamp": transaction.get('timestamp'),
                    "data": data,
                    "transaction_id": transaction.get('transaction_id')
                })
        
        return transactions
    
    def verify_user_vote(self, email, session_id):
        """Verify if a user has voted in a specific session"""
        for block in self.chain:
            if block.index == 0:
                continue
            
            transaction = block.data
            if transaction.get('type') == 'vote':
                vote_data = transaction.get('data', {})
                if (vote_data.get('voter_email') == email and 
                    vote_data.get('session_id') == session_id):
                    return {
                        "verified": True,
                        "block": block.index,
                        "timestamp": transaction.get('timestamp'),
                        "candidate": vote_data.get('candidate_name'),
                        "transaction_id": transaction.get('transaction_id')
                    }
        
        return {"verified": False}
    
    def get_voting_results(self, session_id=None):
        """Get voting results from blockchain"""
        votes = []
        
        for block in self.chain:
            if block.index == 0:
                continue
            
            transaction = block.data
            if transaction.get('type') == 'vote':
                vote_data = transaction.get('data', {})
                
                if session_id is None or vote_data.get('session_id') == session_id:
                    votes.append({
                        "block": block.index,
                        "timestamp": transaction.get('timestamp'),
                        "voter": vote_data.get('voter_email'),
                        "candidate": vote_data.get('candidate_name'),
                        "session": vote_data.get('session_id'),
                        "transaction_id": transaction.get('transaction_id')
                    })
        
        return votes
    
    def print_blockchain_summary(self):
        """Print blockchain summary"""
        print("\n" + "="*60)
        print("BLOCKCHAIN SUMMARY")
        print("="*60)
        
        if not self.chain:
            print("Blockchain is empty")
            return
        
        # Count transaction types
        transaction_counts = {}
        for block in self.chain:
            if block.index > 0:
                tx_type = block.data.get('type', 'unknown')
                transaction_counts[tx_type] = transaction_counts.get(tx_type, 0) + 1
        
        print(f"Total Blocks: {len(self.chain)}")
        print(f"Total Transactions: {len(self.chain) - 1}")
        print(f"Chain Valid: {'✅ Yes' if self.is_chain_valid() else '❌ No'}")
        
        print("\nTransaction Types:")
        for tx_type, count in transaction_counts.items():
            print(f"  {tx_type}: {count}")
        
        print("="*60)
    
    def print_chain_details(self):
        """Print detailed blockchain information"""
        print("\n" + "="*80)
        print("BLOCKCHAIN LEDGER - DETAILED VIEW")
        print("="*80)
        
        for block in self.chain:
            print(f"\n{block}")
            print(f"  Previous Hash: {block.previous_hash[:16]}...")
            print(f"  Timestamp: {block.timestamp}")
            
            if block.index > 0:
                transaction = block.data
                print(f"  Transaction Type: {transaction.get('type', 'N/A').upper()}")
                print(f"  Transaction ID: {transaction.get('transaction_id', 'N/A')}")
                
                data = transaction.get('data', {})
                if transaction.get('type') == 'vote':
                    print(f"  Voter: {data.get('voter_email', 'N/A')}")
                    print(f"  Candidate: {data.get('candidate_name', 'N/A')}")
                    print(f"  Session: {data.get('session_id', 'N/A')}")
                elif transaction.get('type') == 'registration':
                    print(f"  User: {data.get('email', 'N/A')}")
                    print(f"  Username: {data.get('username', 'N/A')}")
                elif transaction.get('type') == 'verification':
                    print(f"  User: {data.get('email', 'N/A')}")
                    print(f"  Action: {data.get('action', 'N/A')}")
            
            print(f"  Hash: {block.hash[:16]}...")
        
        print(f"\nTotal Blocks: {len(self.chain)}")
        print("="*80)