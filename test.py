from PyQt5.QtCore import QThread, pyqtSignal
from operate import *
from daily import Daily

"""
直接使用Daily进行初始化，并使用Daily的方法进行操作
"""


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
        self.index = None

    def update(self, daily: Daily):
        self.daily = daily
        self.operate = Operate(daily.zoom_factor, daily.game_area, self.text_label)
        self.zoom_factor = daily.zoom_factor
        self.game_area = daily.game_area

        self.title_area = get_area(0.02, 0.1, 0.45, 0.05, self.game_area)

    def getNeeds(self, needs, index):
        self.needs = needs
        self.index = index

    def print(self, text, end='\n'):
        print(text, end=end)
        self.text_label.insertPlainText(text + end)

    def mian2help(self):
        self.print('进入raid救援：', end='')
        return self.operate.clickCheck(0.18, 0.725, 'saga_img/raid/团体战救援.png', self.title_area)

    def mian2activity(self):
        self.print('进入活动：', end='')
        return self.operate.clickCheck(0.8, 0.725, 'saga_img/raid/活动.png', self.title_area)

    def activity2raid(self):
        self.print('进入raid召唤：', end='')
        return self.operate.clickCheck(0.8, 0.725, 'saga_img/raid/团体战召唤.png', self.title_area)

    def activity2help(self):
        self.print('进入raid救援：', end='')
        return self.operate.clickCheck(0.4, 0.84, 'saga_img/raid/团体战救援.png', self.title_area)

    def activity2mission(self):
        self.print('进入活动任务：', end='')
        return self.operate.clickCheck(0.2, 0.725, 'saga_img/raid/活动任务.png', self.title_area)

    def activity2box(self):
        self.print('进入扭蛋：', end='')
        return self.operate.clickCheck(0.5, 0.725, 'saga_img/raid/BOX扭蛋.png', self.title_area)

    def mission_choose(self):
        self.print('选择战斗：', end='')
        self.operate.clickR(0.6, 0.2)
        sleep(0.3)
        area = get_area(0.02, 0.175, 0.23, 0.035, self.game_area)
        return self.operate.clickCheck(0.5, 0.3, 'saga_img/daily/综合战斗力.png', area)

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
        self.print('点击参战：', end='')
        if activity:
            area = get_area(0.35, 0.175, 0.3, 0.035, self.game_area)
            return self.operate.clickCheck(0.5, 0.78, 'saga_img/raid/出击确认.png', area)
        else:
            area = get_area(0.35, 0.175, 0.3, 0.035, self.game_area)
            return self.operate.clickCheck(0.5, 0.83, 'saga_img/raid/出击确认.png', area)

    def raid_decide(self, first=True):
        self.print('点击确定：', end='')
        if first:
            area = get_area(0.02, 0.175, 0.23, 0.035, self.game_area)
            return self.operate.clickCheck(0.85, 0.8, 'saga_img/daily/综合战斗力.png', area)
        else:
            area = get_area(0.005, 0.0275, 0.055, 0.03, self.game_area)
            return self.operate.clickCheck(0.8, 0.8, 'saga_img/raid/时钟.png', area)

    def raid_sortie(self):
        self.print('点击出击：', end='')
        area = get_area(0.005, 0.0275, 0.055, 0.03, self.game_area)
        return self.operate.clickCheck(0.85, 0.94, 'saga_img/raid/时钟.png', area)

    def raid_rescue(self):
        self.print('点击救援：', end='')
        area = get_area(0.35, 0.175, 0.3, 0.035, self.game_area)
        if not self.operate.clickCheck(0.71, 0.05, 'saga_img/raid/救援委托.png', area):
            return False
        sleep(0.2)
        self.operate.clickR(0.71, 0.7875)
        return True

    def raid_wait(self):
        self.print('等待战斗结束：', end='')
        area = get_area(0.35, 0.175, 0.3, 0.035, self.game_area)
        return self.operate.waitUntil('saga_img/raid/团体战参加者一览.png', area)

    def check_people(self):
        self.print('人数检查：', end='')
        area = get_area(0.67, 0.748, 0.1, 0.03, self.game_area)
        res = match(area, 'saga_img/raid/一人.png', self.zoom_factor)
        while res < 0.9:
            self.operate.clickR(0.5, 0.4)
            sleep(0.3)
            res = match(area, 'saga_img/raid/一人.png', self.zoom_factor)
            if res < 0.9:
                sleep(0.2)
                self.operate.clickR(0.2, 0.63)
                sleep(0.4)
                self.operate.clickR(0.5, 0.3)
                sleep(0.3)
                res = match(area, 'saga_img/raid/一人.png', self.zoom_factor)
                self.print('.', end='')
            else:
                break
            if match(self.title_area, 'saga_img/raid/团体战救援.png', self.zoom_factor) < 0.9:
                return False
        self.print('成功')
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
        actions = [self.check_people,
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
        self.print('点击抽取：', end='')
        area = get_area(0.35, 0.275, 0.3, 0.035, self.game_area)
        return self.operate.clickCheck(0.67, 0.85, 'saga_img/raid/确认扭蛋.png', area)

    def box_open_confirm(self):
        self.print('点击确认：', end='')
        area = get_area(0.06, 0.026, 0.075, 0.025, self.game_area)
        return self.operate.clickCheck(0.67, 0.6875, 'saga_img/raid/box.png', area)

    def box_reset(self):
        self.print('点击重置：', end='')
        self.operate.clickR(0.75, 0.0875)
        sleep(0.3)
        area = get_area(0.35, 0.275, 0.3, 0.035, self.game_area)
        return self.operate.clickCheck(0.67, 0.6875, 'saga_img/raid/确认.png', area)

    def box_reset_confirm(self):
        self.print('点击确认：', end='')
        self.operate.clickR(0.67, 0.6875)
        sleep(0.3)
        area = get_area(0.35, 0.275, 0.3, 0.035, self.game_area)
        return self.operate.clickCheck(0.67, 0.6875, 'saga_img/raid/选择目标道具.png', area)

    def box_choose(self, index=0):
        x = [0.2, 0.4, 0.6]
        self.print('选择道具：', end='')
        self.operate.clickR(x[index], 0.4125)
        sleep(0.1)
        self.operate.clickR(0.67, 0.6875)
        area = get_area(0.35, 0.275, 0.3, 0.035, self.game_area)
        if match(area, 'saga_img/raid/选择目标道具.png', self.zoom_factor) < 0.9:
            self.print('成功')
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
        if 0 in self.needs:
            self.activity2mission()
            self.mission_choose()
            while self.set_raid_battle():
                sleep(0.5)
        if 1 in self.needs:
            self.activity2help()
            while self.set_raid_help():
                sleep(2)
        if 2 in self.needs:
            self.activity2raid()
            self.operate.clickR(0.5, [0.25, 0.35, 0.45][self.index])
            first = True
            while self.set_raid_sent(first):
                first = False
                sleep(0.5)
        if 3 in self.needs:
            self.activity2box()
            cnt = 0
            while self.set_box():
                cnt += 1
                self.print('完成第%d次扭蛋' % cnt)
                sleep(0.5)

    def run(self):
        self.main()
        self.finished.emit()
