from abc import ABC, abstractmethod


class Hasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def check(self, hashed_password: str, password: str) -> bool:
        pass
