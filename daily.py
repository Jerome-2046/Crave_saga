from PyQt5.QtCore import QThread, pyqtSignal
from operate import *


class Daily(QThread):
    finished = pyqtSignal()

    def __init__(self, zoom_factor: float, game_area: tuple, text_label):
        super().__init__()
        self.operate = Operate(zoom_factor, game_area, text_label)
        self.zoom_factor = zoom_factor
        self.game_area = game_area
        self.text_label = text_label

        self.title_area = get_area(0.02, 0.1, 0.45, 0.05, self.game_area)

        self.needs = None
        self.rooms = None
        self.index = 0
        self.types = None

    def update(self, zoom_factor: float, game_area: tuple):
        self.operate = Operate(zoom_factor, game_area, self.text_label)
        self.zoom_factor = zoom_factor
        self.game_area = game_area

        self.title_area = get_area(0.02, 0.1, 0.45, 0.05, self.game_area)

    def getNeeds(self, needs=None, rooms=None, index=0, types=None):
        self.needs = needs
        self.rooms = rooms
        self.index = index
        self.types = types

    def print(self, text, end='\n'):
        print(text, end=end)
        self.text_label.insertPlainText(text + end)

    def toMain(self):
        print('返回首页：', end='')
        sleep(0.5)
        self.operate.clickR(0.08, 0.95)
        sleep(2)
        print('成功')
        return True

    def mian2explore(self):
        self.print('进入探索：', end='')
        return self.operate.clickCheck(0.6, 0.83, 'saga_img/daily/素材探索.png', self.title_area)

    def exploreRecycle(self):
        area = get_area(0.3, 0.373, 0.4, 0.03, self.game_area)
        self.print('回收队伍：', end='')
        if not self.operate.clickCheck(0.5, 0.75, 'saga_img/daily/获得道具_探索.png', area):
            return False
        sleep(1)
        return self.operate.clickCheck(0.3, 0.95, 'saga_img/daily/素材探索.png', self.title_area)

    def set_explore(self):
        actions = [self.mian2explore, self.exploreRecycle]
        for action in actions:
            if not action():
                return False
        return True

    def mian2mianline(self):
        self.print('进入关卡：', end='')
        return self.operate.clickCheck(0.6, 0.95, 'saga_img/daily/第六章.png', self.title_area)

    def mianline2practiceRoom(self):
        self.print('进入练习室：', end='')
        if not self.operate.clickCheck(0.4, 0.83, 'saga_img/daily/金币收集关卡.png', self.title_area):
            return False
        sleep(0.2)
        return True

    def practiceRoom_gold(self):
        self.print('选择金币收集：', end='')
        return self.operate.clickCheck(0.125, 0.25, 'saga_img/daily/金币收集关卡.png', self.title_area)

    def practiceRoom_role(self):
        self.print('选择魂友育成：', end='')
        return self.operate.clickCheck(0.375, 0.25, 'saga_img/daily/魂友育成关卡.png', self.title_area)

    def practiceRoom_artifact(self):
        self.print('选择神器育成：', end='')
        return self.operate.clickCheck(0.625, 0.25, 'saga_img/daily/神器育成关卡.png', self.title_area)

    def practiceRoom_weapon(self):
        self.print('选择武器育成：', end='')
        return self.operate.clickCheck(0.875, 0.25, 'saga_img/daily/武器育成关卡.png', self.title_area)

    def battle_choose(self, index=0, top=None):
        if top is None:
            top = [0.4, 0.5, 0.6]
        self.print('点击关卡：', end='')
        area = get_area(0.02, 0.175, 0.23, 0.035, self.game_area)
        return self.operate.clickCheck(0.5, top[index], 'saga_img/daily/综合战斗力.png', area)

    def battle_skip(self, times=-1):
        self.print('点击跳过：', end='')
        area = get_area(0.3, 0.235, 0.4, 0.035, self.game_area)
        if not self.operate.clickCheck(0.5, 0.9, 'saga_img/daily/跳过.png', area):
            return False
        if times == -1:
            self.operate.clickR(0.75, 0.48)
        sleep(0.8)
        # TODO
        area = get_area(0.4, 0.925, 0.2, 0.05, self.game_area)
        if not self.operate.clickCheck(0.7, 0.72, 'saga_img/daily/前往下一页.png', area):
            return False
        return True

    def battle_sortie(self, times=1, first=False):
        self.print('点击出击：', end='')
        area = get_area(0.01, 0.025, 0.11, 0.03, self.game_area)
        if first:
            self.operate.clickR(0.67, 0.93, times - 1, 0.05)
            return self.operate.clickCheck(0.85, 0.93, 'saga_img/daily/wave.png', area)
        else:
            return self.operate.clickCheck(0.85, 0.85, 'saga_img/daily/wave.png', area)

    def battle_wait(self):
        self.print('等待战斗结束：', end='')
        area = get_area(0, 0.02, 0.02, 0.04, self.game_area)
        return self.operate.waitUntil('saga_img/daily/蓝色.png', area)

    def battle_settlement(self, keep=False):
        self.print('战斗结算：', end='')
        area = get_area(0.3, 0.058, 0.4, 0.033, self.game_area)
        self.operate.clickUntil(0.5, 0.95, 'saga_img/daily/获得道具.png', area, 0.3, 1.2)
        if not self.operate.clickCheck(0.5, 0.95, 'saga_img/daily/获得道具.png', area):
            return False
        sleep(1.2)
        if keep:
            area = get_area(0.35, 0.235, 0.3, 0.035, self.game_area)
            self.operate.clickR(0.4, 0.95, 3, 0.4)
            if match(area, 'saga_img/daily/AP回复.png', self.zoom_factor) > 0.9:
                # TODO 吃药 self.eatAP(self, type=1, times=3)
                return False
        else:
            self.operate.clickR(0.6, 0.95, 3, 0.3)
        sleep(1)
        return True

    def set_battle_skip(self, times=-1):
        sleep(0.5)
        self.battle_skip(times)
        sleep(0.5)
        self.battle_settlement()
        return True

    def set_practiceRoom(self, rooms=None, index=0):
        if rooms is None:
            rooms = [1, 3]
        actions = [self.mian2mianline,
                   self.mianline2practiceRoom,
                   [[self.practiceRoom_gold, lambda: self.battle_choose(index), self.set_battle_skip],
                    [self.practiceRoom_role, lambda: self.battle_choose(index), self.set_battle_skip],
                    [self.practiceRoom_artifact, lambda: self.battle_choose(index), self.set_battle_skip],
                    [self.practiceRoom_weapon, lambda: self.battle_choose(index), self.set_battle_skip]]]
        for action in actions:
            if callable(action):
                if not action():
                    return False
            else:
                for room in rooms:
                    for sub_action in action[room]:
                        if not sub_action():
                            self.print('失败')
                            return False
        return True

    def mian2guild(self):
        self.print('进入公会：', end='')
        area = get_area(0.02, 0.1, 0.3, 0.05, self.game_area)
        return self.operate.clickCheck(0.75, 0.84, 'saga_img/daily/公会.png', area)

    def guild_support(self):
        self.print('点击应援：', end='')
        self.operate.clickR(0.91, 0.33)
        sleep(0.5)
        self.operate.clickR(0.91, 0.33, 2)
        self.print('成功')
        return True

    def set_guild_support(self):
        actions = [self.mian2guild, self.guild_support]
        for action in actions:
            if not action():
                return False
        return True

    def mian2store(self):
        self.print('进入商店：', end='')
        return self.operate.clickCheck(0.92, 0.95, 'saga_img/daily/商店_1.png', self.title_area)

    def store_store(self):
        self.print('进入商店：', end='')
        sleep(0.5)
        return self.operate.clickCheck(0.12, 0.75, 'saga_img/daily/商店_2.png', self.title_area)

    def store_gold(self):
        self.print('点击金币商店：', end='')
        area = get_area(0.05, 0.18, 0.25, 0.035, self.game_area)
        if match(area, 'saga_img/daily/金币商店.png', self.zoom_factor) > 0.9:
            self.print('成功')
        else:
            area = get_area(0.37, 0.18, 0.25, 0.035, self.game_area)
            if not self.operate.clickCheck(0.5, 0.2, 'saga_img/daily/金币商店.png', area):
                return False
        return True

    def store_buy_all(self, types=None):
        if types is None:
            types = [2]
        self.print('点击批量购买：', end='')
        positions = [[0.05, 0.25], [0.38, 0.25], [0.68, 0.25], [0.05, 0.49], [0.38, 0.49], [0.68, 0.49]]
        for index in types:
            if index == -1:
                break
            self.operate.clickR(positions[index][0], positions[index][1])

        area = get_area(0.3, 0.235, 0.4, 0.035, self.game_area)
        if not self.operate.clickCheck(0.5, 0.75, 'saga_img/daily/批量购买确认.png', area):
            return False
        area = get_area(0.3, 0.235, 0.4, 0.035, self.game_area)
        if not self.operate.clickCheck(0.66, 0.72, 'saga_img/daily/确认购买.png', area):
            return False
        self.operate.clickR(0.5, 0.72)
        return True

    def set_gold_store(self, types=None):
        actions = [self.mian2store,
                   self.store_store,
                   self.store_gold,
                   lambda: self.store_buy_all(types)]
        for action in actions:
            if not action():
                return False
        return True

    def main(self):
        actions = [lambda: self.set_practiceRoom(self.rooms, self.index),
                   self.set_guild_support,
                   self.set_explore,
                   lambda: self.set_gold_store(self.types)]
        for need in self.needs:
            if not actions[need]():
                return False
            self.toMain()
            sleep(2)
        self.print('完成动作')
        return True

    def run(self):
        self.main()
        self.finished.emit()
