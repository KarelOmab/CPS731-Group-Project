from classes.account.account import Account

class User(Account):
    def __init__(self, id: int, username: str):
        super().__init__(id, username)
        self._privileged_mode = False

    @property
    def privileged_mode(self) -> bool:
        """Indicates that a regular user does not have privileged mode."""
        return self._privileged_mode
