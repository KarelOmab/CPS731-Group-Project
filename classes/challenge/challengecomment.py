class ChallengeComment:
    def __init__(self, id, created_at, account_id, is_deleted, challenge_id, title, text, username):
        self._id = id
        self._created_at = created_at
        self._account_id = account_id
        self._is_deleted = is_deleted
        self._challenge_id = challenge_id
        self._title = title
        self._text = text
        self._username = username

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
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def is_deleted(self):
        return self._is_deleted

    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = value

    @property
    def challenge_id(self):
        return self._challenge_id

    @challenge_id.setter
    def challenge_id(self, value):
        self._challenge_id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
