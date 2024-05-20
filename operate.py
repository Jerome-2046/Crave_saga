"""
根据相对位置操作
"""
from pyautogui import moveTo, click, screenshot
from time import sleep
from comparison import match
from reposition import get_position, get_area

delay1 = 10
delay2 = 1.5


class Operate:
    def __init__(self, zoom_factor: float, game_area: tuple, text_label):
        self.zoom_factor = zoom_factor
        self.game_area = game_area
        self.text_label = text_label

    def print(self, text, end='\n'):
        print(str(text), end=end)
        self.text_label.insertPlainText(str(text) + end)

    def clickR(self, left: float, top: float, times=1, delay=0.2):
        """
        点击相对位置
        :param left: 相对水平位置比例（左到右）
        :param top: 相对垂直位置（上到下）
        :param times: 点击次数
        :param delay: 点击间隔
        """
        x, y = get_position(left, top, self.game_area)
        moveTo(x, y)
        for i in range(times):
            click()
            sleep(delay)

    def clickCheck(self, left: float, top: float, path, area, d1=1.0, d2=1.0, d3=0.2, accuracy=0.8, times=5, big=True):
        """
        点击相对位置并根据匹配结果检查是否成功
        :param left: 相对水平位置（左到右）
        :param top: 相对垂直位置（上到下）
        :param path: 目标图像位置
        :param area: 目标区域（相对）
        :param accuracy: 匹配度
        :param d1: 检查前等待时间
        :param d2: 检查间隔
        :param d3: 检查成功后等待时间
        :param times: 尝试次数
        :param big: 是否扩大截图区域
        :return: 是否成功匹配
        """
        self.clickR(left, top)
        for i in range(50):
            result = match(area, path, self.zoom_factor, big)
            sleep(delay1 * d1 / 50)
            if result > accuracy:
                self.print('成功')
                sleep(d3)
                return True
        for i in range(times):
            self.clickR(left, top)
            result = match(area, path, self.zoom_factor, big)
            self.print(i, end=' ')
            if result > accuracy:
                self.print('成功')
                sleep(d3)
                return True
            sleep(delay2 * d2)
        self.print('错误')
        return False

    def waitUntil(self, path, area, delay=0.2, accuracy=0.8, wait=0.3, big=True):
        """
        暂停程序直到识别到某个图像
        :param path: 目标图像位置
        :param area: 目标区域（相对）
        :param delay: 检查匹配延迟间隔
        :param accuracy: 匹配度
        :param wait: 匹配后等待时间
        :param big: 是否扩大截图区域
        :return: 是否成功匹配
        """
        result = match(area, path, self.zoom_factor, big)
        while result < accuracy:
            sleep(delay)
            result = match(area, path, self.zoom_factor, big)
        self.print('成功')
        sleep(wait)
        return True

    def clickUntil(self, left: float, top: float, path, area, d1=0.2, wait=1.0, accuracy=0.8, big=True):
        """
        点击相对位置并根据匹配结果检查是否成功
        :param left: 相对水平位置（左到右）
        :param top: 相对垂直位置（上到下）
        :param path: 目标图像位置
        :param area: 目标区域（相对）
        :param wait: 检查成功后等待时间
        :param d1: 检查前等待时间
        :param accuracy: 匹配度
        :param big: 是否扩大截图区域
        :return: 是否成功匹配
        """
        result = match(area, path, big)
        cnt = 0
        while result < accuracy:
            if cnt > 30:
                break
            self.clickR(left, top)
            sleep(d1)
            result = match(area, path, self.zoom_factor, big)
            cnt += 1
        self.print('成功')
        sleep(wait)
        return True

    def area_test(self, area=None, left: float = None, top: float = None, width: float = None, height: float = None,
                  path='screenshot.png'):
        if not area:
            area = get_area(left, top, width, height, self.game_area)
        else:
            area = get_area(area[0], area[1], area[2], area[3], self.game_area)
        shot = screenshot(region=area)
        shot.save(path)

    def position_test(self, left: float = None, top: float = None):
        x, y = get_position(left, top, self.game_area)
        moveTo(x, y)
