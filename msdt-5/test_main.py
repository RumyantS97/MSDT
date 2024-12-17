

import pytest
from unittest.mock import MagicMock
from main import UserService, UserRepository, User

# Фикстура для реального репозитория (без моков)
@pytest.fixture
def real_repository():
    return UserRepository()

# Фикстура для сервиса с реальным репозиторием
@pytest.fixture
def real_service(real_repository):
    return UserService(real_repository)

# Фикстура для мок-репозитория
@pytest.fixture
def mock_repository():
    return MagicMock(spec=UserRepository)

# Фикстура для сервиса с мок-репозиторием
@pytest.fixture
def mock_service(mock_repository):
    return UserService(mock_repository)

# Тесты без моков
def test_create_user_real(real_service):
    user = real_service.create_user("John Doe", "john.doe@example.com")
    assert user.user_id is not None
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"

def test_get_user_real(real_service):
    user = real_service.create_user("John Doe", "john.doe@example.com")
    fetched_user = real_service.get_user(user.user_id)
    assert fetched_user is not None
    assert fetched_user.name == "John Doe"
    assert fetched_user.email == "john.doe@example.com"

def test_update_user_name_real(real_service):
    user = real_service.create_user("John Doe", "john.doe@example.com")
    real_service.update_user_name(user.user_id, "John Smith")
    updated_user = real_service.get_user(user.user_id)
    assert updated_user.name == "John Smith"

def test_update_user_email_real(real_service):
    user = real_service.create_user("John Doe", "john.doe@example.com")
    real_service.update_user_email(user.user_id, "john.smith@example.com")
    updated_user = real_service.get_user(user.user_id)
    assert updated_user.email == "john.smith@example.com"

def test_get_all_users_real(real_service):
    real_service.create_user("John Doe", "john.doe@example.com")
    real_service.create_user("Jane Doe", "jane.doe@example.com")
    all_users = real_service.get_all_users()
    assert len(all_users) == 2


# Тесты с моками
def test_create_user_mock(mock_service, mock_repository):
    mock_service.create_user("John Doe", "john.doe@example.com")
    mock_repository.add_user.assert_called_once()

def test_update_user_name_mock(mock_service, mock_repository):
    mock_user = User("1", "John Doe", "john.doe@example.com")
    mock_repository.get_user.return_value = mock_user
    mock_service.update_user_name("1", "John Smith")
    assert mock_user.name == "John Smith"
    mock_repository.update_user.assert_called_once()

# Тест с множеством параметров
@pytest.mark.parametrize(
    "name, email, new_name, new_email",
    [
        ("John Doe", "john.doe@example.com", "John Smith", "john.smith@example.com"),
        ("Jane Doe", "jane.doe@example.com", "Jane Smith", "jane.smith@example.com"),
        ("Alice", "alice@example.com", "Alice Johnson", "alice.johnson@example.com"),
    ],
)
def test_update_user_with_parameters(real_service, name, email, new_name, new_email):
    user = real_service.create_user(name, email)
    real_service.update_user_name(user.user_id, new_name)
    real_service.update_user_email(user.user_id, new_email)
    updated_user = real_service.get_user(user.user_id)
    assert updated_user.name == new_name
    assert updated_user.email == new_email