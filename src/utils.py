# utils.py
from PIL import Image
import pyautogui
import numpy as np
import os
import tkinter as tk
from time import  *

import py_win_keyboard_layout

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()

from config import MOVESPEED_PERCENT

def align():
    correct = isCorrectStartPos()
    if correct:
        return
    while not correct:
        aligned = isCorrectStartPos()
        if aligned:
            break

        reset_character()
        sleep(5)

def isCorrectStartPos():
    region = (947, 301, 29, 30)
    location_day: bool = find_exact_color_match("assets/CorrectPosDay.png", region, 40)
    location_night: bool = find_exact_color_match("assets/CorrectPosNight.png", region, 40)

    if location_day or location_night:
        return True
    return False

def start_clicking():
    mouse.press(Button.left)

def stop_clicking():
    mouse.release(Button.left)

def init():
    mouse.scroll(0, 5)
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
    keyboard.press(Key.shift_l)
    sleep(0.05)
    keyboard.release(Key.shift_l)


def get_screen_color(position):
    """
    Возвращает цвет пикселя на экране по координатам.

    :param position: (x, y)
    :return: (R, G, B)
    """
    x, y = position
    # Делаем скриншот одного пикселя
    screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
    # Получаем RGB цвет
    color = screenshot.getpixel((0, 0))
    return color

def find_exact_color_match(image_path, region, accuracy=100, tolerance=10):
    """
    Проверяет совпадение региона экрана с изображением с точностью accuracy%.
    tolerance — максимальное значение суммарного отличия по каналам RGB для совпадения пикселя.

    :param image_path: Путь к PNG-изображению
    :param region: (x, y, width, height)
    :param accuracy: % пикселей для совпадения (1-100)
    :param tolerance: максимальное допустимое отличие (0-765)
    :return: True если совпадение >= accuracy, иначе False
    """
    x, y, w, h = region

    # Загружаем эталонное изображение
    ref_img = Image.open(image_path).convert("RGB")

    # Снимок экрана области
    screenshot = pyautogui.screenshot(region=(x, y, w, h)).convert("RGB")

    os.makedirs("assets", exist_ok=True)
    screenshot.save("assets/DEBUG.png")

    # Проверяем размеры
    if ref_img.size != screenshot.size:
        return False

    ref_np = np.array(ref_img).astype(int)
    shot_np = np.array(screenshot).astype(int)

    diff = np.abs(ref_np - shot_np)
    diff_sum = diff.sum(axis=2)  # сумма по RGB каналам

    # Пиксели считаем совпадающими, если diff_sum <= tolerance
    matches = diff_sum <= tolerance
    match_count = np.sum(matches)
    total_pixels = w * h
    match_percent = (match_count / total_pixels) * 100

    print(f"Match percent: {match_percent:.2f}%")

    return match_percent >= accuracy



def draw_rectangle(region, duration=2):
    """
    Рисует прямоугольник поверх экрана и убирает его через duration секунд.

    :param region: (x, y, width, height)
    :param duration: сколько секунд показывать
    """
    x, y, w, h = region

    root = tk.Tk()
    root.overrideredirect(True)              # без рамок
    root.attributes("-topmost", True)        # поверх всех окон
    root.attributes("-transparentcolor", "white")  # белый — прозрачный

    # Окно по размеру экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Канва
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white", highlightthickness=0)
    canvas.pack()

    # Рисуем прямоугольник (например, красный)
    canvas.create_rectangle(x, y, x + w, y + h, outline="red", width=1)

    # Через duration секунд закрываем окно
    root.after(int(duration * 1000), root.destroy)

    root.mainloop()


def make_screen(region):
    """
    Делает скриншот указанного региона и сохраняет его как assets/Screenshot.png

    :param region: (x, y, width, height)
    """
    x, y, w, h = region

    # Делаем скриншот региона
    screenshot = pyautogui.screenshot(region=(x, y, w, h))

    # Убедимся, что папка assets существует
    os.makedirs("assets", exist_ok=True)

    # Сохраняем
    screenshot.save(os.path.join("assets", "Screenshot.png"))

def reset_character():
    keyboard.press(Key.esc)
    sleep(0.01)
    keyboard.release(Key.esc)
    sleep(0.5)
    keyboard.press('r')
    keyboard.press('к')
    sleep(0.01)
    keyboard.release('r')
    keyboard.release('к')
    sleep(0.5)
    keyboard.press(Key.enter)
    sleep(0.01)
    keyboard.release(Key.enter)

    sleep(0.1)
    mouse.click(Button.left)

def jump():
    keyboard.press(Key.space)
    sleep(0.05)
    keyboard.release(Key.space)
def press(key):
    keyboard.press(key)
    sleep(0.05)
    keyboard.release(key)
def walk(key, time):
    mult = MOVESPEED_PERCENT/100
    keyboard.press(key)
    sleep(time*mult)
    keyboard.release(key)

def is_backpack_full():
    x, y = (1808, 47)
    color = get_screen_color((x, y))
    print(color)
    return color == (140, 39, 39)

def is_backpack_empty():
    x, y = (1617, 47)
    color = get_screen_color((x, y))
    return color == (40,40,40)


def camera_rotate(degree):
    hold_time = abs(degree) / 117.65
    if degree < 0:
        keyboard.press(Key.left)
        sleep(hold_time)
        keyboard.release(Key.left)
    else:
        keyboard.press(Key.right)
        sleep(hold_time)
        keyboard.release(Key.right)