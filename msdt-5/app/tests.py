import pytest
import business_logic as bl

def test_factorial():
    n = 5
    expected = 120

    result = bl.factorial(n)

    assert result == expected

def test_fibonacci():
    n = 10
    expected = 34

    result = bl.fibonacci(n)

    assert result == expected

def test_unique_false():
    assert bl.check_distinct([1,2,3,1,4,2]) == False

def test_unique_true():
    assert bl.check_distinct([1,2,3,5,4,-1]) == True

@pytest.mark.parametrize("a,b,expected", [ ([1,2,3], [4,5,6], 32), ([0,0,1], [1,6,2], 2), ([3,3,3], [3,3,3], 27) ])
def test_scalar_multiplication_parameterized(a, b, expected):
    result = bl.scalar_multiplication(a, b)
    assert result == expected

@pytest.fixture
def matrix():
    matrix = []
    counter = 0
    for i in range(3):
        row = []
        for j in range(3):
            row.append(counter)
            counter += 1
        matrix.append(row)
    return matrix

def test_matrix_rotation(matrix):
    expected = [
        [6, 3, 0],
        [7, 4, 1],
        [8, 5, 2]
    ]
    assert bl.rotate_matrix(matrix) == expected

def test_weather_response():
    def stub_get_current_weather(lat, lon, api_key):
        return {
            "coord": {"lat": lat, "lon": lon},
            "weather": [{id: 800, "main": "Clear", "description": "clear sky"}],
            "main": {"temp": 289.57, "feels_like": 288.78, "humidity": 89, "temp_min": 288.15, "temp_max": 290.15}
        }
    bl.get_current_weather = stub_get_current_weather
    assert stub_get_current_weather(0.34, 0.66, "1234567") == {
            "coord": {"lat": 0.34, "lon": 0.66},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky"}],
            "main": {"temp": 289.57, "feels_like": 288.78, "humidity": 89, "temp_min": 288.15, "temp_max": 290.15}
        }