import cv2
import matplotlib.pyplot as plt
import numpy as np
from logger_config import imageprocessor_logger


def load_image(image_name: str) -> np.ndarray:
    """
    Loads the image according to the specified path, raises an exception if the image file is not found.
    :param image_name: The path with an image.
    :return: The image is in the form of np.ndarray.
    """
    imageprocessor_logger.info("Loading image: %s", image_name)
    img = cv2.imread(image_name)
    if img is None:
        imageprocessor_logger.error("File not found: %s", image_name)
        raise FileNotFoundError("No file with that name was found!")
    imageprocessor_logger.info("Image %s successfully loaded.", image_name)
    return img

def print_image_info(img: np.ndarray) -> None:
    """
    Displays the size of the photo in pixels.
    :param img: The image in the form of np.ndarray.
    :return: None.
    """
    imageprocessor_logger.info("Image dimensions: Height=%d, Width=%d", img.shape[0], img.shape[1])
    print("Height: %d, width: %d" % (img.shape[0], img.shape[1]))

def calc_hist(img: np.ndarray) -> dict:
    """
    Calculates the histogram for a black and white image or
    calculates the brightness histogram and color histograms for a color image.
    :param img: The image in the form of np.ndarray.
    :return: A dictionary containing brightness and color histograms.
    """
    imageprocessor_logger.info("Calculating histogram.")
    hist_dict = {}
    if len(img.shape) == 2:  # Grayscale image
        hist_dict['gray'] = cv2.calcHist([img], [0], None, [256], [0, 256])
    else:  # Color image
        hist_dict['gray'] = cv2.calcHist([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist_dict[color] = cv2.calcHist([img], [i], None, [256], [0, 256])
    imageprocessor_logger.info("Histogram calculation completed.")
    return hist_dict

def dis_hist(hist_dict: dict) -> None:
    """
    Plots the brightness histogram and the color histograms.
    :param hist_dict: A dictionary containing brightness and color histograms.
    :return: None.
    """
    imageprocessor_logger.info("Displaying histograms.")
    plt.figure(figsize=(12, 6))
    if 'gray' in hist_dict:
        ax1 = plt.subplot(1, 2, 1)
        plt.plot(hist_dict['gray'], color='k')
        plt.title('Гистограмма яркости')
        plt.xlim([0, 256])
        plt.xlabel('Интенсивность')
        plt.ylabel('Количество пикселей')

    if any(color in hist_dict for color in ('b', 'g', 'r')):
        plt.subplot(1, 2, 2, sharey=ax1)
        for color in ('b', 'g', 'r'):
            if color in hist_dict:
                plt.plot(hist_dict[color], color=color, label='Канал %s' % color.upper())
        plt.title('Цветовая гистограмма')
        plt.xlim([0, 256])
        plt.xlabel('Интенсивность')
        plt.ylabel('Количество пикселей')
        plt.legend()
    plt.tight_layout()
    plt.show()
    imageprocessor_logger.info("Histograms displayed successfully.")

def resize(img: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resizes the image.
    :param img: The original image in the form of np.ndarray.
    :param width: The width of the photo in pixels.
    :param height: The height of the photo in pixels.
    :return: np.ndarray of the resized image.
    """
    imageprocessor_logger.info("Resizing image to Width=%d, Height=%d.", width, height)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
    imageprocessor_logger.info("Image resized successfully.")
    return resized

def display(img: np.ndarray, resized: np.ndarray) -> None:
    """
    Displays two images in two separate windows at the same time.
    :param img: np.ndarray of the first image.
    :param resized: np.ndarray of the second image.
    :return: None.
    """
    imageprocessor_logger.info("Displaying images.")
    if img is None or resized is None:
        imageprocessor_logger.error("One of the images is None.")
        raise ValueError("One of the images is None.")
    cv2.imshow("Original", img)
    cv2.imshow("Modified", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    imageprocessor_logger.info("Images displayed successfully.")

def save(img: np.ndarray, path: str) -> None:
    """
    Saves the specified image, raises an exception if the image could not be saved.
    :param img: np.ndarray of the image that needs to be saved.
    :param path: The path where the image will be saved.
    :return: None.
    """
    imageprocessor_logger.info("Saving image to %s.", path)
    success = cv2.imwrite(path, img)
    if not success:
        imageprocessor_logger.error("Failed to save image to %s.", path)
        raise IOError("Не удалось сохранить изображение в %s." % path)
    imageprocessor_logger.info("Image saved to %s successfully.", path)
