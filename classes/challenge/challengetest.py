class ChallengeTest:
    def __init__(self, id, challenge_id, is_deleted, test_input, test_output):
        self._id = id
        self._challenge_id = challenge_id
        self._is_deleted = is_deleted
        self._test_input = test_input
        self._test_output = test_output

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def challenge_id(self):
        return self._challenge_id

    @challenge_id.setter
    def challenge_id(self, value):
        self._challenge_id = value

    @property
    def is_deleted(self):
        return self._is_deleted

    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = value

    @property
    def test_input(self):
        return self._test_input

    @test_input.setter
    def test_input(self, value):
        self._test_input = value

    @property
    def test_output(self):
        return self._test_output

    @test_output.setter
    def test_output(self, value):
        self._test_output = value
