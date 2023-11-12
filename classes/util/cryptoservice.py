import hashlib
class CryptoService:
    @staticmethod
    def hash_password(raw_string):
        """
        Generates <some> hash for a given string.

        This function is intended to be used for hashing passwords before storing them in a database.
        It is a one-way process, meaning the original string cannot be retrieved from the hash.

        Args:
            raw_string (str): The raw password string to be hashed.

        Returns:
            str: A hexadecimal digest of the hash

        """
        m = hashlib.sha256()
        m.update(raw_string.encode('utf-8'))
        return  m.hexdigest()
        

