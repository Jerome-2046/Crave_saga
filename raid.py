from PyQt5.QtCore import QThread, pyqtSignal
from operate import *
from daily import Daily


class Riad(QThread):
    finished = pyqtSignal()

    def __init__(self, daily: Daily):
        super().__init__()
        self.daily = daily
        self.operate = Operate(daily.zoom_factor, daily.game_area, daily.text_label)
        self.zoom_factor = daily.zoom_factor
        self.game_area = daily.game_area
        self.text_label = daily.text_label

        self.title_area = get_area(0.02, 0.1, 0.45, 0.05, self.game_area)

        self.needs = None

    def update(self, daily: Daily):
        self.daily = daily
        self.operate = Operate(daily.zoom_factor, daily.game_area, self.text_label)
        self.zoom_factor = daily.zoom_factor
        self.game_area = daily.game_area

        self.title_area = get_area(0.02, 0.1, 0.45, 0.05, self.game_area)

    def getNeeds(self, needs: int):
        self.needs = needs

    def print(self, text, end='\n'):
        print(text, end=end)
        self.text_label.insertPlainText(text + end)

    def mian2help(self):
        print('进入raid救援：', end='')
        return self.operate.clickCheck(80, 580, 'saga_img/raid/团体战救援.png', self.title_area)

    def mian2activity(self):
        print('进入活动：', end='')
        return self.operate.clickCheck(380, 580, 'saga_img/activity/活动.png', self.title_area)

    def activity2raid(self):
        print('进入raid召唤：', end='')
        return self.operate.clickCheck(380, 560, 'saga_img/raid/团体战召唤.png', self.title_area)

    def activity2help(self):
        print('进入raid救援：', end='')
        return self.operate.clickCheck(180, 670, 'saga_img/raid/团体战救援.png', self.title_area)

    def activity2mission(self):
        print('进入活动任务：', end='')
        return self.operate.clickCheck(70, 560, 'saga_img/activity/活动任务.png', self.title_area)

    def mission_choose(self):
        print('选择战斗：', end='')
        self.operate.clickR(1, 1)
        sleep(0.3)
        return self.daily.battle_choose()

    def set_raid_battle(self):
        flag = True
        actions = [lambda: self.daily.battle_sortie(4, flag),
                   self.daily.battle_wait,
                   lambda: self.daily.battle_settlement(True)]
        while True:
            for action in actions:
                if not action():
                    return False
                flag = False
                sleep(0.4)

    def raid_enter(self, activity=True):
        print('点击参战：', end='')
        if activity:
            area = get_area(150, 143, 150, 27, self.game_area)
            return self.operate.clickCheck(225, 630, 'saga_img/raid/出击确认.png', area)
        else:
            area = get_area(150, 143, 150, 27, self.game_area)
            return self.operate.clickCheck(225, 670, 'saga_img/raid/出击确认.png', area)

    def raid_decide(self, first=True):
        print('点击确定：', end='')
        if first:
            area = get_area(10, 143, 100, 25, self.game_area)
            return self.operate.clickCheck(380, 640, 'saga_img/daily/综合战斗力.png', area)
        else:
            area = get_area(3, 28, 27, 24, self.game_area)
            return self.operate.clickCheck(380, 640, 'saga_img/raid/时钟.png', area)

    def raid_sortie(self):
        print('点击出击：', end='')
        area = get_area(3, 28, 27, 24, self.game_area)
        return self.operate.clickCheck(380, 750, 'saga_img/raid/时钟.png', area)

    def raid_rescue(self):
        print('点击救援：', end='')
        area = get_area(150, 143, 150, 27, self.game_area)
        if not self.operate.clickCheck(320, 40, 'saga_img/raid/救援委托.png', area):
            return False
        sleep(0.2)
        self.operate.clickR(320, 630)
        return True

    def raid_wait(self):
        print('等待战斗结束：', end='')
        area = get_area(150, 143, 150, 27, self.game_area)
        return self.operate.waitUntil('saga_img/raid/团体战参加者一览.png', area)

    def checkPeople(self):
        print('人数检查：', end='')
        area = get_area(280, 599, 60, 17, self.game_area)
        res = match(area, 'saga_img/raid/一人.png', self.zoom_factor)
        while res < 0.9:
            self.operate.clickR(225, 320)
            sleep(0.3)
            res = match(area, 'saga_img/raid/一人.png', self.zoom_factor)
            if res < 0.9:
                sleep(0.2)
                self.operate.clickR(90, 500)
                sleep(0.4)
                self.operate.clickR(225, 240)
                sleep(0.3)
                res = match(area, 'saga_img/raid/一人.png', self.zoom_factor)
                print('.', end='')
            else:
                break
            if match(self.title_area, 'saga_img/raid/团体战救援.png', self.zoom_factor) < 0.9:
                return False
        print('成功')
        sleep(0.4)
        return True

    def set_raid_sent(self, first=True):
        if first:
            actions = [self.raid_enter,
                       lambda: self.raid_decide(first),
                       self.raid_sortie,
                       self.raid_rescue,
                       self.raid_wait,
                       lambda: self.daily.battle_settlement(True)]
        else:
            actions = [lambda: self.raid_decide(first),
                       self.raid_rescue,
                       self.raid_wait,
                       lambda: self.daily.battle_settlement(True)]
        for action in actions:
            if not action():
                return False
            sleep(0.3)
        return True

    def set_raid_help(self):
        actions = [self.checkPeople,
                   lambda: self.raid_enter(False),
                   self.raid_decide,
                   self.raid_sortie,
                   self.raid_wait,
                   self.daily.battle_settlement]
        for action in actions:
            if not action():
                return False
            sleep(0.1)
        return True

    def box_open(self):
        print('点击抽取：', end='')
        area = get_area(150, 224, 150, 27, self.game_area)
        return self.operate.clickCheck(300, 680, 'saga_img/raid/确认扭蛋.png', area)

    def box_open_confirm(self):
        print('点击确认：', end='')
        area = get_area(29, 29, 34, 20, self.game_area)
        return self.operate.clickCheck(300, 550, 'saga_img/raid/box.png', area)

    def box_reset(self):
        print('点击重置：', end='')
        self.operate.clickR(350, 70)
        sleep(0.3)
        area = get_area(150, 224, 150, 27, self.game_area)
        return self.operate.clickCheck(350, 70, 'saga_img/raid/确认.png', area)

    def box_reset_confirm(self):
        print('点击确认：', end='')
        self.operate.clickR(300, 550)
        sleep(0.3)
        area = get_area(150, 224, 150, 27, self.game_area)
        return self.operate.clickCheck(300, 550, 'saga_img/raid/选择目标道具.png', area)

    def box_choose(self, index=0):
        x = [90, 180, 270]
        print('选择道具：', end='')
        self.operate.clickR(x[index], 330)
        sleep(0.1)
        self.operate.clickR(300, 550)
        area = get_area(150, 224, 150, 27, self.game_area)
        if match(area, 'saga_img/raid/选择目标道具.png', self.zoom_factor) < 0.9:
            print('成功')
            return True
        return False

    def set_box(self):
        actions = [self.box_open,
                   self.box_open_confirm,
                   self.box_reset,
                   self.box_reset_confirm,
                   self.box_choose]
        for action in actions:
            if not action():
                return False
            sleep(0.3)
        return True

    def main(self):
        # mode = int(input('点击回车开始'))
        # position_test(350, 70)
        # modes = [3]
        # modes = [4]
        # modes = [1, 2]
        modes = [2]
        if 1 in modes:
            while self.set_raid_help():
                pass
            sleep(1)
            self.operate.clickR(400, 100)
            sleep(2)
            self.operate.clickR(200, 280)
        if 2 in modes:
            first = True
            while self.set_raid_sent(first):
                first = False
                pass
        if 3 in modes:
            while self.set_raid_battle():
                pass
        if 4 in modes:
            cnt = 0
            while self.set_box():
                cnt += 1
                print(cnt)
