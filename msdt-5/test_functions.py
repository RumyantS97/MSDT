import os
import pytest
import time
from user import UserDataFetcher, User, Calculator, Database, RandomDataGenerator, Timer, save_to_file, load_from_file


def test_fetch_data_success(mocker):  
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "John", "age": 30}
    
    mocker.patch('requests.get', return_value=mock_response)
    
    api_url = "https://api.example.com/user/1"
    fetcher = UserDataFetcher(api_url)
    
    data = fetcher.fetch_data()
    
    assert data == {"name": "John", "age": 30}
    mock_response.json.assert_called_once()


def test_fetch_data_failure(mocker): 
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    
    mocker.patch('requests.get', return_value=mock_response)
    
    api_url = "https://api.example.com/user/1"
    fetcher = UserDataFetcher(api_url)
    
    with pytest.raises(Exception, match="Failed to fetch data"):
        fetcher.fetch_data()


def test_process_data_valid(mocker):  
    fetcher = UserDataFetcher(api_url="")
    data = {"name": "John", "age": 30}
    
    processed_data = fetcher.process_data(data)
    
    assert processed_data == {"name": "JOHN", "age": 60}
    
    
def test_process_data_invalid(mocker): 
    fetcher = UserDataFetcher(api_url="")
    
    with pytest.raises(ValueError, match="Invalid data format"):
        fetcher.process_data({"name": "John"}) 
        
        
def test_calculate_sum():
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_user_info():
    user = User("John", 25)
    assert user.get_info() == {"name": "John", "age": 25}


def test_is_adult():
    user = User("Alice", 17)
    assert not user.is_adult()
    
    user = User("Bob", 18)
    assert user.is_adult()


def test_empty_input():
    calc = Calculator()
    assert calc.add(0, 0) == 0

@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (5, 7, 12), (0, 0, 0)])
def test_calculate_sum_parametrized(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected


def test_invalid_file_load():
    with pytest.raises(Exception, match="File non_existent_file.json not found"):
        load_from_file("non_existent_file.json")


def test_random_user_generation():
    random_user = RandomDataGenerator.generate_random_user()
    assert random_user.name in ["John", "Jane", "Alice", "Bob", "Charlie"]
    assert 18 <= random_user.age <= 99


def test_random_number_generation():
    random_number = RandomDataGenerator.generate_random_number()
    assert 1 <= random_number <= 100


def test_timer():
    timer = Timer()
    timer.start()
    time.sleep(1)
    elapsed = timer.stop()
    assert elapsed >= 1


def test_save_load_file():
    data = {"name": "John", "age": 30}
    filename = "test_data.json"
    save_to_file(data, filename)
    loaded_data = load_from_file(filename)
    assert loaded_data == data
    os.remove(filename)


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero"):
        calc.divide(10, 0)


def test_add_user_to_database():
    db = Database()
    user = User("Test User", 25)
    db.add_user("123", user)
    assert db.get_user("123").get_info() == {"name": "Test User", "age": 25}


def test_remove_user_from_database():
    db = Database()
    user = User("Test User", 25)
    db.add_user("123", user)
    db.remove_user("123")
    with pytest.raises(KeyError):
        db.get_user("123")


if __name__ == "__main__":
    pytest.main(["-v"])
