#tailrec fun
import json
def factorial(n, accum = 1):
    return accum if n <= 1 else factorial(n - 1, accum * n)


def fibonacci(n):
    arr = [1, 1]
    for i in range(2, n):
        arr.append(arr[i - 1] + arr[i - 2])
    return arr[n - 1]


def check_distinct(lst):
    return len(lst) == len(set(lst))


def scalar_multiplication(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def rotate_matrix(matrix):
    n = len(matrix)
    
    # Шаг 1: Транспонирование матрицы
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Шаг 2: Переворот каждой строки
    for i in range(n):
        matrix[i].reverse()
    return matrix

def get_current_weather(lat, lon, api_key):
    # Для отсутствия ошибок компиляции заменю взаимодействие с интернетом на простое чтение файла
    with open('weather.json', 'r', encoding= 'utf-8') as file:
        data = file.read()
    
    weather_data = json.loads(data)
    
    for weather in weather_data['list']:
        if weather['coord']['lat'] == lat and weather['coord']['lon'] == lon:
            return weather['weather'][0]['description']
    
    return 'No weather data found for given coordinates'