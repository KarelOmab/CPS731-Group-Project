from classes.account.account import Account

class User(Account):
    def __init__(self, id: int, username: str):
        super().__init__(id, username)
        self._privileged_mode = False
