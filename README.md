# Voting System with Blockchain Verification

A secure online voting system with blockchain-based vote integrity verification.

## Features
- User registration/login with OTP
- Voting verification with ID upload
- Admin voting session management
- Blockchain vote verification
- Tamper-proof vote recording
- Real-time results with blockchain validation

## Installation
1. Install Python 3.8+
2. Install MySQL/XAMPP
3. Run: `python setup.py`
4. Run: `python main.py`

## Database Setup
The system uses MySQL with these tables:
- users, voting_verification, voting_sessions
- candidates, votes, otp_codes, blockchain_blocks

## Blockchain Features
- Vote hashing and blockchain storage
- Proof of Work mining (difficulty: 4)
- Vote integrity verification
- Blockchain audit tools
- Tamper detection system

## Configuration
Edit `config.py` for:
- Database credentials
- Email settings (for OTP)
- Admin credentials
- Blockchain difficulty
