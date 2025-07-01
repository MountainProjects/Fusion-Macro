import os
from PIL import Image, ImageGrab
import pyautogui
import numpy as np
import var
import cv2

class Screen():
    def __init__(self, Macro):
        self.Macro = Macro

    def is_backpack_full(self):
        x, y = (1808, 47)
        color = self.get_screen_color((x, y))
        return color == (140, 39, 39)

    def is_backpack_empty(self):
        x, y = (1617, 47)
        color = self.get_screen_color((x, y))
        return color == (40,40,40)

    def isCorrectStartPos(self):
        screen_width, screen_height = 1920, 1080  # или твоя функция получения размера

        center_x = screen_width // 2

        # Зона: ширина 200 пикселей, вся высота
        region = (
            center_x - 100,
            0,
            center_x + 100,
            screen_height
        )
        
        day_score = self.find_template_similarity("src/assets/CorrectPosDay.png", region)
        night_score = self.find_template_similarity("src/assets/CorrectPosNight.png", region)

        print(f"DAY: {day_score*100}%")
        print(f"NIGHT: {night_score*100}%")

        if day_score >= 0.5 or night_score >= 0.5:
            return True        
        else:
            return False

        
    def find_template_similarity(self, template_path, region):
        # Загружаем шаблон
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template_h, template_w = template.shape[:2]

        # Делаем скриншот региона
        screenshot = ImageGrab.grab(bbox=region)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Сопоставляем шаблон
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return max_val

    def get_screen_color(self, position):
        """
        Возвращает цвет пикселя на экране по координатам.

        :param position: (x, y)
            :return: (R, G, B)
        """
        x, y = position
        screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
        color = screenshot.getpixel((0, 0))
        return color

    def find_image_on_region(self, image_path, region):
        """
        Возвращает процент совпадения области на экране с указанным изображением
        :param image_path: Путь к PNG-изображению
        :param region: (x, y, width, height)
        """
        x, y, width, height = region

        total_pixels = width * height

        img = Image.open(image_path).convert("RGB")

        screenshot = pyautogui.screenshot(region=(x,y, width, height)).convert("RGB")

         #ТЕСТ ФУНКЦИЯ ДЛЯ СКРИНА ТОГО ЧТО ОНО ПРОВЕРЯЕТ (ДЕБАГ)
        screenshot.save("src/assets/DEBUG.png")

        if img.size != screenshot.size:
            return False
        
        img_numpy = np.array(img).astype(int)
        screen_numpy = np.array(screenshot).astype(int)

        difference = np.abs(img_numpy - screen_numpy)
        differency_sum = difference.sum(axis=2)

        matches = differency_sum <= 10 # Я ХЗ 10 ЭТО ТИПА tolerance мне чат гпт так сказал
        match_count = np.sum(matches)

        match_percent = (match_count / total_pixels)

        return match_percent

    def make_screenshot(self, region, save:bool = True):
        x, y, width, height = region

        screenshot = pyautogui.screenshot(region=(x,y, width, height))
        
        if save:
            os.makedirs("assets", exist_ok=True)
            screenshot.save(os.path.join("src/assets", "Screenshot.png"))
            return
        else:
            return screenshot