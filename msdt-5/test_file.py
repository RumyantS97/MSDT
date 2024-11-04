import numpy as np
import pytest
from PIL import Image
from mock.mock import patch
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
    original = np.array([[0, 0], [0, 0]])
    compressed = np.array([[0, 0], [0, 0]])
    assert Lab05.calculate_psnr(original, compressed) == 100


def test_alternative_psnr_calculation():
    c = np.array([[255, 255], [255, 255]])
    cw = np.array([[0, 0], [0, 0]])
    assert np.isclose(Lab05.calculate_psnr_alternative(c, cw), 0)


def test_proximity_calculation():
    cvz1 = np.array([1, 2, 3])
    cvz2 = np.array([4, 5, 6])
    proximity = Lab05.calculate_proximity(cvz1, cvz2)
    expected_proximity = (np.dot(cvz1, cvz2) /
                          (np.linalg.norm(cvz1) * np.linalg.norm(cvz2)))
    assert np.isclose(proximity, expected_proximity)


def test_false_proximity_generation():
    count = 5
    vectors = Lab05.generate_false_detection_vectors(count)
    assert len(vectors) == count
    for vector in vectors:
        assert vector.shape == (65536,)


@pytest.mark.parametrize("m", [3, 5, 7])
def test_smooth_and_calculate_proximity(m):
    np.random.seed(42)
    CVZ = np.random.normal(0, 1, size=[256, 256])
    reverse_image = np.random.rand(256, 256)
    phase_array = np.angle(np.fft.fft2(reverse_image))
    original_abs_spectrum = abs(np.fft.fft2(reverse_image))
    ALPHA = 1

    result = Lab05.smooth_and_calculate_proximity(m)
    assert isinstance(result, float), "Result should be a floating-point number"
    assert -1 <= result <= 1, "Proximity must be in range [-1, 1]"

    if m > 3:
        smaller_window_result = (
            Lab05.smooth_and_calculate_proximity(m - 2))
        assert result != pytest.approx(
            smaller_window_result, rel=1e-4
        ), (
            f"Results with m={m} and m={m-2} should differ, "
            "indicating that smoothing has an effect."
        )


def test_detect_false_proximity():
    cvz = np.array([1, 2, 3, 4, 5])

    false_detection_cvz = [
        np.array([1, 2, 3, 4, 5]),
        np.array([2, 3, 4, 5, 6]),
        np.array([-1, -2, -3, -4, -5]),
        np.array([1, 2, 3, 4, 0]),
    ]

    def mock_calculate_proximity(cvz1, cvz2):
        return 1.0

    with patch(
            'Lab05.calculate_proximity',
            side_effect=mock_calculate_proximity
    ):
        false_detection_proximity_array = (
            Lab05.detect_false_proximity(false_detection_cvz, cvz)
        )

    assert (len(false_detection_cvz) ==
            len(false_detection_proximity_array))
    assert false_detection_proximity_array == [1, 1, 1, 1]


@pytest.fixture
def setup_image():
    img_array = np.ones((512, 512), dtype=np.uint8) * 128
    img = Image.fromarray(img_array)
    return img

@pytest.fixture
def mock_reverse_image(mocker, setup_image):
    return mocker.patch('Lab05.Image.open', return_value=setup_image)

def test_compress_jpeg_and_calculate_proximity(
        mocker, mock_reverse_image):
    qf = 50
    mocker.patch('Lab05.reverse_image', mock_reverse_image)
    proximity = Lab05.compress_jpeg_and_calculate_proximity(qf)

    assert isinstance(proximity, float)
    assert -1 <= proximity <= 1
    mock_reverse_image.assert_called_once_with("JPEG_image.jpg")