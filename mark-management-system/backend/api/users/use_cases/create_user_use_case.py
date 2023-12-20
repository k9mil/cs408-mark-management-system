from api.users.repositories.user_repository import UserRepository

from api.system.models.models import User

from api.system.schemas.schemas import UserCreate


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, request: UserCreate) -> None:
        if self.user_repository.find_by_email(request.email_address):
            raise Exception("User already exists")
        
        hashed_password = request.password + "this_is_a_test"

        user = User(
            reg_no="this_is_a_test",
            email_address=request.email_address,
            first_name=request.first_name,
            last_name=request.last_name,
            password=hashed_password
        )

        self.user_repository.add(user)

        return user
