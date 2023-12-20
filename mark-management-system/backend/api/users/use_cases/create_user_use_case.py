from faker import Faker

from api.users.repositories.user_repository import UserRepository

from api.system.models.models import User

from api.system.schemas.schemas import UserCreate

from api.users.hashers.bcrypt_hasher import BCryptHasher


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, bcrypt_hasher: BCryptHasher, faker: Faker):
        self.user_repository = user_repository
        self.bcrypt_hasher = bcrypt_hasher
        self.faker = faker
    
    def execute(self, request: UserCreate) -> None:
        if self.user_repository.find_by_email(request.email_address):
            raise Exception("User already exists")
        
        hashed_password = self.bcrypt_hasher.hash(request.password)

        user = User(
            reg_no=f"{self.faker.random_lowercase_letter()}{self.faker.random_lowercase_letter()}{self.faker.random_lowercase_letter()}{self.faker.random_number(5)}",
            email_address=request.email_address,
            first_name=request.first_name,
            last_name=request.last_name,
            password=hashed_password
        )

        self.user_repository.add(user)

        return user
