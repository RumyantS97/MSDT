import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def display_image(img: Image):
    root = tk.Tk()
    root.title("Просмотр изображения")

    try:
        # Масштабирование изображения, сохраняя пропорции
        max_width = 800  # Максимальная ширина изображения
        max_height = 600 # Максимальная высота изображения
        width, height = img.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height))

        # Преобразование изображения в формат Tkinter
        photo = ImageTk.PhotoImage(img)

        # Создание метки для отображения изображения
        label = ttk.Label(root, image=photo)
        label.image = photo  # Указание на фото, чтобы избежать сборки мусора
        label.pack()
        root.mainloop()

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
