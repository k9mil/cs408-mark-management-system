from faker import Faker

from api.system.models.models import User

from api.system.schemas.schemas import UserCreate
from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_already_exists import UserAlreadyExists

from api.users.hashers.bcrypt_hasher import BCryptHasher


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, bcrypt_hasher: BCryptHasher, faker: Faker):
        self.user_repository = user_repository
        self.bcrypt_hasher = bcrypt_hasher
        self.faker = faker
    
    def execute(self, request: UserCreate) -> UserSchema:
        if self.user_repository.find_by_email(request.email_address):
            raise UserAlreadyExists("User already exists")
        
        hashed_password = self.bcrypt_hasher.hash(request.password)

        user = User(
            email_address=request.email_address,
            first_name=request.first_name,
            last_name=request.last_name,
            password=hashed_password
        )

        self.user_repository.add(user)

        return user
