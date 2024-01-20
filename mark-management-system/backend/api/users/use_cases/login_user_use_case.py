from api.system.models.models import User

from api.system.schemas.schemas import UserLogin
from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound
from api.users.errors.invalid_credentials import InvalidCredentials

from api.users.hashers.bcrypt_hasher import BCryptHasher


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, bcrypt_hasher: BCryptHasher):
        self.user_repository = user_repository
        self.bcrypt_hasher = bcrypt_hasher
    
    def execute(self, request: UserLogin) -> UserSchema:
        user = self.user_repository.find_by_email(request.email_address)

        if user is None:
            raise UserNotFound("User not found")
        
        if not self.bcrypt_hasher.check(user.password, request.password):
            raise InvalidCredentials("Invalid Credentials provided")
        
        return user
