import cv2
import matplotlib.pyplot as plt
import numpy as np

def load_image(image_name: str) -> np.ndarray:
    """
    Loads the image according to the specified path, raises an exception if the image file is not found.
    :param image_name: The path with an image.
    :return: The image is in the form of np.ndarray
    """
    img = cv2.imread(image_name)
    if img is None:
        raise FileNotFoundError("No file with that name was found!")
    return img

def print_image_info(img: np.ndarray) -> None:
    """
    Displays the size of the photo in pixels
    :param img: The image is in the form of np.ndarray
    :return: None
    """
    print(f"Height: {img.shape[0]}, width: {img.shape[1]}")


def calc_hist(img: np.ndarray) -> dict:
    """
    Calculates the histogram for a black and white image or
    calculates the brightness histogram and color histograms for a color image.
    :param img: The image in the form of np.ndarray
    :return: A dictionary containing brightness and color histograms.
    """
    hist_dict = {}
    if len(img.shape) == 2:  # Grayscale image
        hist_dict['gray'] = cv2.calcHist([img], [0], None, [256], [0, 256])
    else:  # Color image
        hist_dict['gray'] = cv2.calcHist([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist_dict[color] = cv2.calcHist([img], [i], None, [256], [0, 256])
    return hist_dict

def dis_hist(hist_dict: dict) -> None:
    """
    Plots the brightness histogram and the color histograms.
    :param hist_dict: A dictionary containing brightness and color histograms.
    :return: None
    """
    plt.figure(figsize=(12, 6))

    if 'gray' in hist_dict:  # Гистограмма яркости
        ax1 = plt.subplot(1, 2, 1)
        plt.plot(hist_dict['gray'], color='k')
        plt.title('Гистограмма яркости')
        plt.xlim([0, 256])
        plt.xlabel('Интенсивность')
        plt.ylabel('Количество пикселей')

    if any(color in hist_dict for color in ('b', 'g', 'r')):  # Цветовые гистограммы
        plt.subplot(1, 2, 2, sharey=ax1)
        for color in ('b', 'g', 'r'):
            if color in hist_dict:
                plt.plot(hist_dict[color], color=color, label=f'Канал {color.upper()}')
        plt.title('Цветовая гистограмма')
        plt.xlim([0, 256])
        plt.xlabel('Интенсивность')
        plt.ylabel('Количество пикселей')
        plt.legend()
    plt.tight_layout()
    plt.show()

def resize(img: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resizes the image.
    :param img: The original image is in the form of np.ndarray
    :param width: The width of the photo in pixels
    :param height: The height of the photo in pixels
    :return: np.ndarray of the resized image.
    """
    # scale_percent = 50
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
    return resized

def display(img: np.ndarray, resized: np.ndarray) -> None:
    """
    Displays two images in two separate windows at the same time.
    :param img: np.ndarray of a first image.
    :param resized: np.ndarray of a second image.
    :return: None
    """
    if img is None:
        raise ValueError("Error: Image 1 has not been founded.")
    elif resized is None:
        raise ValueError("Error: Image 2 has not been founded.")
    else:
        cv2.imshow("Original", img)
        cv2.imshow("Modified", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def save(img: np.ndarray, path: str) -> None:
    """
    Saves the specified image, raises an exception if the image could not be saved.
    :param img: np.ndarray of an image, that needs to be saved.
    :param path: The path where the image will be saved
    :return: None
    """
    success = cv2.imwrite(path, img)
    if not success:
        raise IOError(f"Не удалось сохранить изображение в {path}.")
