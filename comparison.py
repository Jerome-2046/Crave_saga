"""
根据截图对比
"""
from pyautogui import screenshot
import cv2
from numpy import array, fromfile, uint8

baseZoomFactor = 1.5


def bigger(area: tuple, x=2, y=4):
    return int(area[0] - x), int(area[1] - y), int(area[2] + 2 * x), int(area[3] + 2 * y)


def match(area: tuple, path: str, zoom_factor: float, big: bool = True):
    area = bigger(area) if big else area
    shot = screenshot(region=area)
    source = cv2.cvtColor(array(shot), cv2.COLOR_RGB2BGR)
    target = cv2.imdecode(fromfile(path, dtype=uint8), -1)
    target = cv2.resize(target, (
        int(target.shape[1] * zoom_factor / baseZoomFactor), int(target.shape[0] * zoom_factor / baseZoomFactor)))
    return cv2.minMaxLoc(cv2.matchTemplate(source, target, cv2.TM_CCOEFF_NORMED))[1]
