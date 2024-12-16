import cv2   #обработка
import numpy as np   #массивы
import matplotlib.pyplot as plt
 
# "C:/Users/teori/Downloads/nia.jpg"   "C:/Users/teori/Favorites/scale_1200.jfif"
# Загрузка исходного изображения
input_image_path = "C:/Users/teori/Downloads/nia.jpg"
image = cv2.imread(input_image_path)

# Перевод изображения в оттенки серого (Задание 1)
# Преобразование в оттенки серого по формуле
def weighted_grayscale(image):
    r = image[:,:,2] #красный канал
    g = image[:,:,1] #зеленый канал
    b = image[:,:,0] #синий канал
    gray = 0.3 * r + 0.59 * g + 0.11 * b
    gray = gray.astype(np.uint8) # Преобразуем в 8-битное целое без знака
    return gray

gray_image = weighted_grayscale(image)

# Препарирование изображения: яркостный срез с сохранением фона (Задание 2)
# Препарирование изображения: преобразование яркости (Задание 2 - модифицировано)
def transformation_b(image):
    transformed_image = np.zeros_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pixel_value = image[y, x]
            if pixel_value < 50:
                transformed_image[y, x] = pixel_value
            elif pixel_value > 200:
                transformed_image[y, x] = 255 - (pixel_value - 200)
            else:
                transformed_image[y, x] = pixel_value * 2  #Умножение
    transformed_image = np.clip(transformed_image, 0, 255).astype(np.uint8) # Обрезаем до 0-255
    return transformed_image

transformed_image = transformation_b(gray_image)

# Фильтр повышения контрастности (Задание 3)
kernel = np.array([[0, -1, 0],
                   [-1, 8, -1],
          [0, -1, 0]])
kernel = kernel / 4 #нормализация 
A = 0
B = 0.25

def apply_filter(image, kernel, A, B):
    filtered_image = cv2.filter2D(image, -1, kernel)
    filtered_image = filtered_image + B
    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image

contrast_image = apply_filter(gray_image, kernel, A, B)


# Добавление шума "соль-перец"
def add_salt_and_pepper_noise(image, amount=0.02):
    noisy_image = image.copy()
    num_salt = np.ceil(amount * image.size * 0.5)
    num_pepper = np.ceil(amount * image.size * 0.5)

    # Добавляем "соль" (белые точки)
    coords_salt = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[tuple(coords_salt)] = 255

    # Добавляем "перец" (чёрные точки)
    coords_pepper = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[tuple(coords_pepper)] = 0

    return noisy_image

noisy_image = add_salt_and_pepper_noise(gray_image)

# Отображение всех изображений в интерфейсе (одновременное отображение 4-х)
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0, 0].set_title("Исходное изображение")
axs[0, 0].axis("off")


axs[0, 1].imshow(gray_image, cmap="gray")
axs[0, 1].set_title("Оттенки серого")
axs[0, 1].axis("off")

axs[1, 0].imshow(transformed_image, cmap="gray")
axs[1, 0].set_title("Яркостный срез (Препарирование)")
axs[1, 0].axis("off")

axs[1, 1].imshow(contrast_image, cmap="gray")
axs[1, 1].set_title("Фильтр повышения контрастности")
axs[1, 1].axis("off")

plt.tight_layout()
plt.show()
