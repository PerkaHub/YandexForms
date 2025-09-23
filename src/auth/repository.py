from src.repository.base import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository[User]):
    model = User
