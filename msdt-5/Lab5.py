class SearchElement:
    def find(self, array, target):
        left, right = 0, len(array) - 1
        while left <= right:
            mid = (left + right) // 2
            if array[mid] == target:
                return mid
            elif array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def parse_input(self, input_string):
        try:
            return list(map(int, map(str.strip, input_string.split(','))))
        except ValueError:
            raise ValueError("Некорректный формат входных данных.")

def main():
    search = SearchElement()
    
    try:
        input_array = input("Введите массив целых чисел через запятую: ")
        array = search.parse_input(input_array)
        
        if not array:
            raise ValueError("Массив не должен быть пустым.")
        
        target_input = input("Введите число для поиска: ")
        
        if not target_input.strip():
            raise ValueError("Целое число для поиска не было введено.")
        
        target = int(target_input)
        
        result = search.find(sorted(array), target)  
        
        if result >= 0:
            print(f"Элемент найден на позиции: {result}")
        else:
            print("Элемент не найден в массиве.")
    
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
