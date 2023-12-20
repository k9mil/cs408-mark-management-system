from bcrypt import hashpw, checkpw, gensalt

from api.users.hashers.hasher import Hasher


class BCryptHasher(Hasher):
    def hash(self, password: str) -> str:
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    def check(self, hashed_password: str, password: str) -> bool:
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))