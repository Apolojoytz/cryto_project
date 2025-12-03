# Package initialization
# Export the main functions for easy access
from .login import login
from .register import register
from .verification_voting import voting_verification
from .voting import vote
from .logout import logout

__all__ = ['login', 'register', 'voting_verification', 'vote', 'logout']