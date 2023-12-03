from abc import ABC

class Account(ABC):
    def __init__(self, id: int, username: str):
        self._id = id
        self._username = username

    @property
    def id(self) -> int:
        """Getter for the account's ID."""
        return self._id
    
    @property
    def username(self) -> str:
        """Getter for the account's username."""
        return self._username
    
    @property
    def privileged_mode(self) -> bool:
        """Indicates that a moderator has privileged mode enabled."""
        return self._privileged_mode
    
    def __str__(self) -> str:
        return f"id:{self.id}, username:{self.username}, privileged_mode:{self.privileged_mode}"
