class ChallengeSubmission:
    def __init__(self, id, created_at, challenge_id, account_id, exec_time, exec_chars, exec_src):
        self._id = id
        self._created_at = created_at
        self._challenge_id = challenge_id
        self._account_id = account_id
        self._exec_time = exec_time
        self._exec_chars = exec_chars
        self._exec_src = exec_src

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def challenge_id(self):
        return self._challenge_id

    @challenge_id.setter
    def challenge_id(self, value):
        self._challenge_id = value

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def exec_time(self):
        return self._exec_time

    @exec_time.setter
    def exec_time(self, value):
        self._exec_time = value

    @property
    def exec_chars(self):
        return self._exec_chars

    @exec_chars.setter
    def exec_chars(self, value):
        self._exec_chars = value

    @property
    def exec_src(self):
        return self._exec_src

    @exec_src.setter
    def exec_src(self, value):
        self._exec_src = value
