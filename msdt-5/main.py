import uuid
from typing import Optional, List


class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def update_name(self, new_name: str):
        self.name = new_name

    def update_email(self, new_email: str):
        self.email = new_email


class UserRepository:
    def __init__(self):
        self.users = {}

    def add_user(self, user: User):
        if user.user_id in self.users:
            raise ValueError("User with this ID already exists.")
        self.users[user.user_id] = user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def update_user(self, user: User):
        if user.user_id not in self.users:
            raise ValueError("User with this ID does not exist.")
        self.users[user.user_id] = user

    def get_all_users(self) -> List[User]:
        return list(self.users.values())


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, name: str, email: str) -> User:
        user_id = str(uuid.uuid4())
        user = User(user_id, name, email)
        self.user_repository.add_user(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repository.get_user(user_id)

    def update_user_name(self, user_id: str, new_name: str):
        user = self.user_repository.get_user(user_id)
        if user:
            user.update_name(new_name)
            self.user_repository.update_user(user)
        else:
            raise ValueError("User not found.")

    def update_user_email(self, user_id: str, new_email: str):
        user = self.user_repository.get_user(user_id)
        if user:
            user.update_email(new_email)
            self.user_repository.update_user(user)
        else:
            raise ValueError("User not found.")

    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all_users()


