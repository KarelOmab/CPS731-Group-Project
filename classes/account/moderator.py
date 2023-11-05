from classes.account.account import Account

class Moderator(Account):
    def __init__(self, id: int, username: str):
        super().__init__(id, username)
        self._privileged_mode = True

    @property
    def privileged_mode(self) -> bool:
        """Indicates that a moderator has privileged mode enabled."""
        return self._privileged_mode
