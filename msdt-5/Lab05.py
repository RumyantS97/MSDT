import logging
from math import log10, sqrt, pi
import random


logging.basicConfig(
    filename="logger.log", level="INFO",
    format="%(asctime)s %(levelname)s Line: %(lineno)d %(message)s"
)

ALPHA = 1
CVZ = [[random.gauss(0, 1) for _ in range(256)] for _ in range(256)]


def process_threshold(x):
    """
    Applies a threshold to the input value x.
    """
    result = 1 if x > 0.1 else 0
    logging.info(f"Applied threshold to {x}, result: {result}")
    return result


def calculate_psnr(original, compressed):
    """
    Calculates the Peak Signal-to-Noise Ratio between the original and compressed images.
    """
    mse = sum((o - c) ** 2 for row_o, row_c in zip(original, compressed)
              for o, c in zip(row_o, row_c)) / (len(original) * len(original[0]))
    if mse == 0:
        logging.warning("MSE is zero. PSNR value is set to 100")
        return 100
    max_pixel = 255.0
    psnr_value = 20 * log10(max_pixel / sqrt(mse))
    logging.info(f"Calculated PSNR: {psnr_value}")
    return psnr_value



def calculate_psnr_alternative(c, cw):
    """
    Alternative method to calculate the PSNR.
    """
    psnr_value = 10 * log10(255**2 / (sum((ci - cwi) ** 2 for ci, cwi in zip(c, cw)) / len(c)))
    logging.info(f"Calculated alternative PSNR: {psnr_value}")
    return psnr_value


def select_best_alpha(image):
    """
    Selects the best alpha value automatically by maximizing PSNR.
    """
    psnr = 0
    best_alpha = 0
    best_proximities = 0
    logging.info("Selecting best alpha")
    for alpha in range(1, 1001, 100):
        logging.info(f"Testing alpha: {alpha}")
        image_array = [[int(image[i][j]) for j in range(len(image[i]))] for i in
                       range(len(image))]  # Convert the image to the frequency domain using FFT
        spectre_array = fft2(image_array)
        phase_array = [get_phase(x) for x in spectre_array]

        abs_spectrum = [[abs(x) for x in row] for row in spectre_array]
        original_abs_spectrum = abs_spectrum
        modified_abs_spectrum = [row[:] for row in abs_spectrum]
        for i in range(128, 384):
            for j in range(128, 384):
                modified_abs_spectrum[i][j] = abs_spectrum[i][j] + ALPHA * CVZ[i][j]

        modified_spectrum = multiply_spectra(modified_abs_spectrum, phase_array)
        reverse_array = ifft2(modified_spectrum)
        reverse_image = reverse_array  # Save image without PIL

        new_psnr = calculate_psnr_alternative(image_array, reverse_array)
        if new_psnr > psnr:
            psnr = new_psnr
            best_alpha = alpha
            logging.info(f"Found new best alpha: {best_alpha}, PSNR: {psnr}")
    return best_alpha, psnr

def generate_false_detection_vectors(count):
    """
    Generates a list of false detection vectors (CVZ) with the specified count.
    """
    false_detection_cvz = []
    for i in range(count):
        false_detection_cvz.append([random.gauss(0, 1) for _ in range(65536)])
    return false_detection_cvz


def calculate_proximity(first_cvz, second_cvz):
    """
    Calculates the proximity between two vectors.
    """
    numerator = sum(f * s for f, s in zip(first_cvz, second_cvz))
    denominator = sqrt(sum(f ** 2 for f in first_cvz) * sum(s ** 2 for s in second_cvz))
    return numerator / denominator


def detect_false_proximity(false_detection_cvz, cvz):
    """
    Detects the proximity of false CVZ vectors relative to the given CVZ vector.
    """
    false_detection_proximity_array = []
    for false_cvz in false_detection_cvz:
        false_detection_proximity_array.append(calculate_proximity(cvz, false_cvz))
    logging.info(f"False detection proximities: {false_detection_proximity_array}")
    return false_detection_proximity_array


def rotate_and_calculate_proximity(rotation_angle, image_array):
    """
    Rotates the image by an angle and gets the proximity
    """
    rotated_image = rotate_image(image_array, rotation_angle)
    spectre_array = fft2(rotated_image)
    reverse_array = ifft2(spectre_array)
    reverse_spectre_array = fft2(reverse_array)
    reverse_abs_spectrum = [[abs(x) for x in row] for row in reverse_spectre_array]

    rotated_cvz = [[reverse_abs_spectrum[i][j] - CVZ[i][j] / ALPHA for j in range(128, 384)] for i in range(128, 384)]
    flattened_rotated_cvz = flatten(rotated_cvz)
    flattened_cvz = flatten(CVZ)
    p = calculate_proximity(flattened_cvz, flattened_rotated_cvz)

    logging.info(f"Proximity after rotation by {rotation_angle} degrees: {p}")
    return p


def apply_cut_and_calculate_proximity(replacement_proportion, original_array, reverse_array):
    """
    Change part of reversed image with part of original image and calculate proximity
    """
    size = len(reverse_array)
    for i in range(int(replacement_proportion * size)):
        for j in range(int(replacement_proportion * size)):
            reverse_array[i][j] = original_array[i][j]

    spectre_array = fft2(reverse_array)
    reverse_array = ifft2(spectre_array)
    reverse_spectre_array = fft2(reverse_array)
    reverse_abs_spectrum = [[abs(x) for x in row] for row in reverse_spectre_array]

    cut_cvz = [[reverse_abs_spectrum[i][j] - CVZ[i][j] / ALPHA for j in range(128, 384)] for i in range(128, 384)]
    flattened_cut_cvz = flatten(cut_cvz)
    flattened_cvz = flatten(CVZ)
    p = calculate_proximity(flattened_cvz, flattened_cut_cvz)

    logging.info(f"Proximity after applying cut with {replacement_proportion} proportion: {p}")
    return p


def smooth_and_calculate_proximity(m, reverse_image):
    """
    Applies smoothing with a window of given size and calculates proximity.
    """
    smooth_array = smooth_image(reverse_image, m)
    spectre_array = fft2(smooth_array)
    reverse_array = ifft2(spectre_array)
    reverse_spectre_array = fft2(reverse_array)
    reverse_abs_spectrum = [[abs(x) for x in row] for row in reverse_spectre_array]

    max_size = min(len(reverse_abs_spectrum), len(reverse_abs_spectrum[0]), len(CVZ), len(CVZ[0]))
    smoothed_cvz = [[reverse_abs_spectrum[i][j] - CVZ[i][j] / ALPHA for j in range(128, max_size)] for i in
                    range(128, max_size)]
    flattened_smoothed_cvz = flatten(smoothed_cvz)
    flattened_cvz = flatten(CVZ)
    p = calculate_proximity(flattened_cvz, flattened_smoothed_cvz)

    logging.info(f"Proximity after smoothing with {m} window size: {p}")
    return p


def compress_jpeg_and_calculate_proximity(jpeg_quality, original_image_array):
    """
    Compresses the image to JPEG with the specified quality factor and calculates proximity.
    """
    compressed_image_array = simulate_jpeg_compression(original_image_array, jpeg_quality)

    # Вычисляем близость между оригинальным и сжатыми изображениями
    proximity = calculate_proximity(original_image_array, compressed_image_array)

    # Логирование результата
    logging.debug(f"JPEG сжатие с качеством {jpeg_quality}, близость: {proximity}")

    return proximity


def simulate_jpeg_compression(image_array, quality):
    """
    Имитация сжатия изображения в формате JPEG путём уменьшения точности данных пикселей.
    """
    # Сжатие понизит точность данных. Уменьшаем диапазон значений пикселей.
    scale_factor = 255 / quality  # Чем меньше качество, тем больше сжатие
    compressed_image = [
        [round(pixel / scale_factor) * scale_factor for pixel in row]
        for row in image_array
    ]
    return compressed_image

# Functions for handling FFT and other operations
def fft2(array):
    """
    Fast Fourier Transform 2D.
    """
    # Simple FFT implementation using DFT
    return [[complex(0, 0) for _ in range(len(array[0]))] for _ in range(len(array))]  # Placeholder

def ifft2(spectre_array):
    """
    Inverse Fast Fourier Transform 2D.
    """
    return [[0 for _ in range(len(spectre_array[0]))] for _ in range(len(spectre_array))]  # Placeholder

def get_phase(spectre_value):
    """
    Returns the phase of a complex number
    """
    return pi / 2  # Placeholder for actual phase calculation

def multiply_spectra(abs_spectrum, phase_array):
    """
    Multiplies magnitude and phase to get the complex spectrum.
    """
    return [[0 for _ in range(len(abs_spectrum[0]))] for _ in range(len(abs_spectrum))]  # Placeholder

def flatten(matrix):
    """
    Flattens a 2D matrix into a 1D array.
    """
    return [elem for row in matrix for elem in row]

def rotate_image(image_array, angle):
    """
    Rotates an image by the given angle (in degrees).
    """
    return image_array  # Placeholder for image rotation logic

def smooth_image(image_array, filter_size=3):
    # Высчитываем отступы для работы с краями
    height = len(image_array)
    width = len(image_array[0])

    # Создаем пустое изображение для хранения результата
    smoothed_image = [[0] * width for _ in range(height)]

    # Размер фильтра (filter_size) предполагает использование его центра, чтобы обрабатывать пиксели
    offset = filter_size // 2

    for i in range(height):
        for j in range(width):
            # Собираем значения пикселей из окрестности для текущего пикселя
            neighbors = []

            # Проходим по окрестности (квадрат с размером filter_size)
            for di in range(-offset, offset + 1):
                for dj in range(-offset, offset + 1):
                    ni, nj = i + di, j + dj
                    # Проверяем, чтобы индексы не выходили за пределы изображения
                    if 0 <= ni < height and 0 <= nj < width:
                        neighbors.append(image_array[ni][nj])

            # Среднее значение пикселей из окрестности
            smoothed_image[i][j] = sum(neighbors) // len(neighbors)

    return smoothed_image

# flatten_CVZ = CVZ.flatten()
# false_detection_cvz = generate_false_detection_vectors(100)
# false_detection_proximity_array = (
#     detect_false_proximity(false_detection_cvz, CVZ.flatten()))

# x = np.arange(0, 100, 1)
# y = false_detection_proximity_array
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.plot(x, y, color="red")
# plt.show()

# logging.info("Loading image and converting to array")
# image = Image.open("bridge.tif")
# image_array = np.asarray(image)
#
# logging.info("Transforming image to frequency domain")
# spectre_array = np.fft.fft2(image_array)
# get_phase = np.vectorize(phase)
# phase_array = get_phase(spectre_array)
# abs_spectrum = abs(spectre_array)
# original_abs_spectrum = abs(spectre_array)
#
# logging.info("Embedding CVZ into image")
# modified_abs_spectrum = abs_spectrum
# modified_abs_spectrum[128:384, 128:384] = (
#         abs_spectrum[128:384, 128:384] + ALPHA*CVZ)
# modified_spectrum = modified_abs_spectrum * np.exp(phase_array*1j)
# reverse_array = abs(np.fft.ifft2(modified_spectrum))
# reverse_image = Image.fromarray(reverse_array)
# reverse_image.convert("RGB").save("img_with_cvz.png")
#
# logging.info("Evaluating embedded CVZ")
# new_image = Image.open("img_with_cvz.png").convert("L")
# reverse_array = np.asarray(new_image)
# save_reverse_array = reverse_array
# reverse_array = save_reverse_array.copy()
# reverse_spectre_array = np.fft.fft2(reverse_array)
# reverse_abs_spectrum = abs(reverse_spectre_array /
#                           np.exp(phase_array*1j))
# included_cvz = (reverse_abs_spectrum[128:384, 128:384] -
#                 original_abs_spectrum[128:384, 128:384]) / ALPHA
# flatten_cvz = CVZ.flatten()
# flatten_included_cvz = included_cvz.flatten()
# p = (sum(flatten_cvz*flatten_included_cvz) /
#      (((sum(flatten_cvz**2))**(1/2)) *
#       ((sum(flatten_included_cvz**2))**(1/2))))
# included_cvz_estimation = process_threshold(p)
# logging.info(f"Threshold p-value for included CVZ: {p}, inclusion estimation: {included_cvz_estimation}")
# reverse_image = Image.fromarray(reverse_array)
#
#
# # CUT
# logging.info("Starting CUT analysis")
# cut_param_array = np.arange(0.55, 1.45, 0.15)
# cut_proximities = []
# for cut_param in cut_param_array:
#     proximity = apply_cut_and_calculate_proximity(cut_param)
#     cut_proximities.append(proximity)
#     logging.debug(f"CUT parameter: {cut_param}, proximity: {proximity}")
#
#
# # ROTATION
# logging.info("Starting ROTATION analysis")
# rotation_param_array = np.arange(1, 90, 8.9)
# rotation_proximities = []
# for rotation_param in rotation_param_array:
#     proximity = rotate_and_calculate_proximity(rotation_param)
#     rotation_proximities.append(proximity)
#     logging.debug(f"ROTATION parameter: {rotation_param}, proximity: {proximity}")
#
#
# # SMOOTH
# logging.info("Starting SMOOTH analysis")
# smooth_param_array = np.arange(3, 15, 2)
# smooth_proximities = []
# for smooth_param in smooth_param_array:
#     proximity = smooth_and_calculate_proximity(smooth_param)
#     smooth_proximities.append(proximity)
#     logging.debug(f"SMOOTH parameter: {smooth_param}, proximity: {proximity}")
#
#
# # JPEG
# logging.info("Starting JPEG compression analysis")
# jpeg_param_array = np.arange(30, 91, 10)
# jpeg_proximities = []
# for jpeg_param in jpeg_param_array:
#     proximity = compress_jpeg_and_calculate_proximity(int(jpeg_param))
#     jpeg_proximities.append(proximity)
#     logging.debug(f"JPEG quality parameter: {jpeg_param}, proximity: {proximity}")


# # OUTPUT
# logging.info("Construction CUT process graph")
# x = cut_param_array
# y = cut_proximities
# plt.title("CUT")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.plot(x, y, color="red")
# plt.show()
#
# logging.info("Construction ROTATION process graph")
# x = rotation_param_array
# y = rotation_proximities
# plt.title("ROTATION")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.plot(x, y, color="red")
# plt.show()
#
# logging.info("Construction SMOOTH process graph")
# x = smooth_param_array
# y = smooth_proximities
# plt.title("SMOOTH")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.plot(x, y, color="red")
# plt.show()
#
# logging.info("Construction JPEG process graph")
# x = jpeg_param_array
# y = jpeg_proximities
# plt.title("JPEG")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.plot(x, y, color="red")
# plt.show()