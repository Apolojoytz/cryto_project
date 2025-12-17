# voting_system/blockchain/voting_blockchain.py
import hashlib
import json
from datetime import datetime
from .blockchain import blockchain_instance
from database.db_connection import execute_query

class VotingBlockchain:
    def __init__(self):
        self.blockchain = blockchain_instance
        # Load existing blockchain if available
        self.blockchain.load_from_file()
    
    def record_vote(self, session_id, user_email, candidate_id, candidate_name):
        """Record a vote on the blockchain"""
        # Get additional verification data
        user_query = "SELECT username, voting_verified FROM users WHERE email = %s"
        user_data = execute_query(user_query, (user_email,), fetch_one=True)
        
        if not user_data:
            return None
        
        # Create vote record for blockchain
        vote_data = {
            "type": "vote",
            "session_id": session_id,
            "user_email_hash": self.hash_email(user_email),  # Hash for privacy
            "username": user_data['username'],
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "timestamp": str(datetime.now()),
            "voting_verified": user_data['voting_verified'],
            "metadata": {
                "recorded_at": str(datetime.now()),
                "record_type": "vote_cast"
            }
        }
        
        # Add to blockchain
        block = self.blockchain.add_block(vote_data)
        
        # Save blockchain
        self.blockchain.save_to_file()
        
        # Also store block hash in database for quick verification
        self.store_block_reference(block.hash, "vote", user_email, session_id)
        
        return block.hash
    
    def record_session_creation(self, session_id, session_name, admin_email):
        """Record voting session creation on blockchain"""
        session_data = {
            "type": "session_creation",
            "session_id": session_id,
            "session_name": session_name,
            "admin_email_hash": self.hash_email(admin_email),
            "timestamp": str(datetime.now()),
            "metadata": {
                "recorded_at": str(datetime.now()),
                "record_type": "session_created"
            }
        }
        
        block = self.blockchain.add_block(session_data)
        self.blockchain.save_to_file()
        self.store_block_reference(block.hash, "session", admin_email, session_id)
        
        return block.hash
    
    def record_user_verification(self, user_email, verification_data):
        """Record user verification on blockchain"""
        verification_block = {
            "type": "user_verification",
            "user_email_hash": self.hash_email(user_email),
            "verification_data": {
                "fullname": verification_data.get('fullname'),
                "gender": verification_data.get('gender'),
                "phone_hash": self.hash_string(verification_data.get('phone', '')),
                "timestamp": str(datetime.now())
            },
            "metadata": {
                "recorded_at": str(datetime.now()),
                "record_type": "verification_completed"
            }
        }
        
        block = self.blockchain.add_block(verification_block)
        self.blockchain.save_to_file()
        self.store_block_reference(block.hash, "verification", user_email)
        
        return block.hash
    
    def hash_email(self, email):
        """Hash email for privacy (SHA256)"""
        return hashlib.sha256(email.encode()).hexdigest()
    
    def hash_string(self, text):
        """Hash any string (SHA256)"""
        if not text:
            return ""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def store_block_reference(self, block_hash, record_type, identifier, reference_id=None):
        """Store blockchain reference in database"""
        try:
            query = """
            INSERT INTO blockchain_references 
            (block_hash, record_type, identifier, reference_id, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            """
            result = execute_query(query, (block_hash, record_type, identifier, reference_id))
            
            if not result:
                print(f"⚠️  Could not save blockchain reference to database")
            return result
        except Exception as e:
            print(f"⚠️  Could not save blockchain reference: {e}")
            print(f"   Table 'blockchain_references' might not exist")
            print(f"   Run: python setup.py to create the table")
            return None
    
    def verify_vote(self, user_email, session_id):
        """Verify if a vote is recorded on blockchain"""
        # Hash the email for lookup
        email_hash = self.hash_email(user_email)
        
        # Search blockchain for this vote
        for block in self.blockchain.chain:
            if block.data.get("type") == "vote":
                if (block.data.get("user_email_hash") == email_hash and 
                    block.data.get("session_id") == session_id):
                    return {
                        "found": True,
                        "block_index": block.index,
                        "block_hash": block.hash,
                        "timestamp": block.timestamp,
                        "candidate": block.data.get("candidate_name")
                    }
        
        return {"found": False}
    
    def get_blockchain_info(self):
        """Get blockchain information"""
        return {
            "chain_length": len(self.blockchain.chain),
            "is_valid": self.blockchain.is_chain_valid(),
            "latest_block": self.blockchain.get_latest_block().to_dict() if self.blockchain.chain else None,
            "difficulty": self.blockchain.difficulty
        }
    
    def validate_all_votes(self):
        """Validate all votes in the blockchain"""
        votes = []
        for block in self.blockchain.chain:
            if block.data.get("type") == "vote":
                votes.append({
                    "block_index": block.index,
                    "session_id": block.data.get("session_id"),
                    "user_email_hash": block.data.get("user_email_hash"),
                    "candidate": block.data.get("candidate_name"),
                    "timestamp": block.timestamp,
                    "block_hash": block.hash
                })
        
        return {
            "total_votes": len(votes),
            "votes": votes,
            "blockchain_valid": self.blockchain.is_chain_valid()
        }

# Initialize voting blockchain
voting_blockchain = VotingBlockchain()