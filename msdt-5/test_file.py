import pytest
import Lab05

@pytest.mark.parametrize('threshold_arg, threshold_result', [
    (0, 0),
    (0.1, 0),
    (0.101, 1),
    (1, 1)
])
def test_threshold(threshold_arg, threshold_result):
    assert Lab05.process_threshold(threshold_arg) == threshold_result


def test_psnr_calculation():
    original = [[0, 0], [0, 0]]
    compressed = [[0, 0], [0, 0]]

    result = Lab05.calculate_psnr(original, compressed)
    assert result == 100


def test_alternative_psnr_calculation():
    c = [255, 255]
    cw = [0, 0]

    result = Lab05.calculate_psnr_alternative(c, cw)
    assert result == 0


def test_proximity_calculation():
    cvz1 = [1, 2, 3]
    cvz2 = [4, 5, 6]

    result = Lab05.calculate_proximity(cvz1, cvz2)
    expected_proximity = sum(cvz1[i] * cvz2[i] for i in range(len(cvz1))) / (
            (sum(x ** 2 for x in cvz1) ** 0.5) * (sum(x ** 2 for x in cvz2) ** 0.5)
    )
    assert result == expected_proximity


def test_false_proximity_generation():
    count = 5
    vectors = Lab05.generate_false_detection_vectors(count)

    assert len(vectors) == count
    for vector in vectors:
        assert len(vector) == 65536


@pytest.mark.parametrize("m", [3, 5, 7])
def test_smooth_and_calculate_proximity(m):
    reverse_image = [[0 for _ in range(256)] for _ in range(256)]  # Пример случайного изображения
    result = Lab05.smooth_and_calculate_proximity(m, reverse_image)
    assert result is not None  # Пример проверки


def test_detect_false_proximity():
    cvz = [1, 2, 3, 4, 5]
    false_detection_cvz = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [-1, -2, -3, -4, -5],
        [1, 2, 3, 4, 0],
    ]

    # Мокируем функцию calculate_proximity
    def mock_calculate_proximity(cvz1, cvz2):
        return 1.0

    Lab05.calculate_proximity = mock_calculate_proximity  # Переопределяем функцию

    false_detection_proximity_array = Lab05.detect_false_proximity(false_detection_cvz, cvz)

    assert len(false_detection_cvz) == len(false_detection_proximity_array), (
        f"Expected {len(false_detection_cvz)} proximity values, got {len(false_detection_proximity_array)}"
    )
    assert false_detection_proximity_array == [1, 1, 1,
                                               1], f"Expected [1, 1, 1, 1], got {false_detection_proximity_array}"


@pytest.fixture
def setup_image():
    img_array = [[128 for _ in range(512)] for _ in range(512)]  # 512x512 изображение
    return img_array

@pytest.fixture
def mock_reverse_image():
    # Создаём изображение или возвращаем необходимые данные для теста
    return [[0 for _ in range(256)] for _ in range(256)]

def test_compress_jpeg_and_calculate_proximity(mock_reverse_image):
    qf = 50
    original_image_array = [[128 for _ in range(512)] for _ in range(512)]  # Пример изображения

    # Симуляция сжатия JPEG
    compressed_image_array = Lab05.simulate_jpeg_compression(original_image_array, qf)

    result = Lab05.calculate_proximity(original_image_array, compressed_image_array)

    assert isinstance(result, float), f"Expected a float, got {type(result)}"
    assert -1 <= result <= 1, f"Expected result to be between -1 and 1, got {result}"