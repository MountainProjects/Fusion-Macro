import os
from PIL import Image
import pyautogui
import numpy as np

class Screen():
    def __init__(self, Macro):
        self.Macro = Macro

    def isCorrectStartPos(self):
        region = (947, 301, 29, 30)
        location_day: bool = find_exact_color_match("assets/CorrectPosDay.png", region, 40)
        location_night: bool = find_exact_color_match("assets/CorrectPosNight.png", region, 40)

        return (location_day or location_night)    
    
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

        # ТЕСТ ФУНКЦИЯ ДЛЯ СКРИНА ТОГО ЧТО ОНО ПРОВЕРЯЕТ (ДЕБАГ)
        #screenshot.save("assets/DEBUG.png")

        if img.size != screenshot.size:
            return False
        
        img_numpy = np.array(img).astype(int)
        screen_numpy = np.array(screenshot).astype(int)

        difference = np.abs(img_numpy - screen_numpy)
        differency_sum = differency_sum(axis=2)

        matches = difference <= 10 # Я ХЗ 10 ЭТО ТИПА tolerance мне чат гпт так сказал
        match_count = np.sum(matches)

        match_percent = (match_count / total_pixels)

        return match_percent

    def make_screenshot(self, region:(), save:bool = True):
        x, y, width, height = region

        screenshot = pyautogui.screenshot(region=(x,y, width, height))
        
        if save:
            os.makedirs("assets", exist_ok=True)
            screenshot.save(os.path.join("src/assets", "Screenshot.png"))
            return
        else:
            return screenshot