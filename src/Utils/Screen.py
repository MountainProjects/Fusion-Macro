import os
from PIL import Image, ImageGrab
import pyautogui
import numpy as np
import var
import cv2
import threading
import time

class Screen():
    def __init__(self, Macro):
        self.SpeedTemplates = {}
        self.speed_buff = 0
        self.speed_thread = None
        for file in os.listdir("src/assets/speeds"):
            if file.endswith(".png") or file.endswith(".jpg"):
                speed = int(os.path.splitext(file)[0])
                path = os.path.join("src/assets/speeds", file)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                self.SpeedTemplates[speed] = img

        self.Macro = Macro

    def is_backpack_full(self):
        x, y = (1905, 110)
        color = self.get_screen_color((x, y))
        return color == (80, 24, 24)

    def is_backpack_empty(self):
        x, y = (1716, 110)
        color = self.get_screen_color((x, y))
        return color == (40,40,40)

    def isCorrectStartPos(self):

        RECT_WIDTH = 80
        RECT_HEIGHT = 270
        OFFSET_X = 10
        OFFSET_Y = -240


        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Прямоугольник из твоих настроек
        left   = center_x - RECT_WIDTH // 2 + OFFSET_X
        top    = center_y - RECT_HEIGHT // 2 + OFFSET_Y
        right  = left + RECT_WIDTH
        bottom = top + RECT_HEIGHT

        region = (left, top, right, bottom)

        score = self.find_template_similarity("src/assets/CenterPos.png", region)

        print(f"CENTER: {score*100:.2f}%")

        return score >= 0.9



        
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

    def task_spawn(self, func, *args):
        thread = threading.Thread(target=func, args=args, daemon=True)
        thread.start()
        return thread

    def start_speed_thread(self):
        self.stop_speed_check = False
        self.speed_thread = self.task_spawn(self.speed_check_loop)

    def stop_speed_thread(self):
        self.stop_speed_check = True
        if self.speed_thread and self.speed_thread.is_alive():
            self.speed_thread.join(timeout=1.0)

    def speed_check_loop(self):
        """Бесконечный цикл проверки скорости"""
        while not self.stop_speed_check and getattr(self.Macro, 'started', True):
            self.speed_buff = self.get_speed_buff()
            time.sleep(0.2)  # Проверяем каждые 0.5 секунды

    def get_speed_buff(self):
        OFFSET_X = 0
        OFFSET_Y = 0
        WIDTH = 200
        HEIGHT = 100
        THRESHOLD = 0.97

        screenshot = pyautogui.screenshot(region=(OFFSET_X, pyautogui.size()[1]-OFFSET_Y-HEIGHT, WIDTH, HEIGHT))
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        best_val = 0
        best_speed = 0
        best_loc = (0, 0)

        for speed, template in self.SpeedTemplates.items():
            res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val > best_val:
                best_val = max_val
                best_speed = speed
                best_loc = max_loc

        if best_val < THRESHOLD:
            return 0
        return best_speed

    def find_image_on_region(self, image_path, region, is_debug: bool = False):
        import datetime

        x, y, width, height = region
        total_pixels = width * height

        img = Image.open(image_path).convert("RGB")
        screenshot = pyautogui.screenshot(region=(x, y, width, height)).convert("RGB")

        if is_debug:
            os.makedirs("src/assets", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot.save(f"src/assets/DEBUG_{timestamp}.png")

        if img.size != screenshot.size:
            return False

        img_numpy = np.array(img).astype(int)
        screen_numpy = np.array(screenshot).astype(int)

        difference = np.abs(img_numpy - screen_numpy)
        differency_sum = difference.sum(axis=2)

        matches = differency_sum <= 10  # tolerance
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