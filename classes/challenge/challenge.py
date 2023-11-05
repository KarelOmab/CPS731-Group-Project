class Challenge():
    def __init__(self, id, created_at, account_id, is_deleted, name, difficulty, description, stub_name, stub_block, time_allowed_sec):
        self._id = id
        self._created_at = created_at
        self._account_id = account_id
        self._is_deleted = is_deleted
        self._name = name
        self._difficulty = difficulty
        self._description = description
        self._stub_name = stub_name
        self._stub_block = stub_block
        self._time_allowed_sec = time_allowed_sec
        self._challenge_tests = []

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @property
    def account_id(self):
        return self._account_id
    
    @property
    def is_deleted(self):
        return self._is_deleted

    @property
    def name(self):
        return self._name

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def description(self):
        return self._description

    @property
    def stub_name(self):
        return self._stub_name

    @property
    def stub_block(self):
        return self._stub_block

    @property
    def time_allowed_sec(self):
        return self._time_allowed_sec

    @property
    def challenge_tests(self):
        return self._challenge_tests

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = value

    @name.setter
    def name(self, value):
        self._name = value

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

    @description.setter
    def description(self, value):
        self._description = value

    @stub_name.setter
    def stub_name(self, value):
        self._stub_name = value

    @stub_block.setter
    def stub_block(self, value):
        self._stub_block = value

    @time_allowed_sec.setter
    def time_allowed_sec(self, value):
        self._time_allowed_sec = value

    @challenge_tests.setter
    def challenge_tests(self, value):
        self._challenge_tests = value
