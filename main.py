import os
import sys

from PyQt5.QtCore import Qt, QUrl, QTimer, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDockWidget, QPushButton, QTextEdit, QVBoxLayout, \
    QGridLayout, QMenu, QAction, QTabWidget, QCheckBox, QButtonGroup, QLabel

from daily import Daily
from test import Riad
from operate import Operate


def addButton(layout: QGridLayout, text, callback, row, col, row_span=1, col_span=1):
    button = QPushButton(text)
    button.clicked.connect(callback)
    # button.setFixedSize(140, 40)
    layout.addWidget(button, row, col, row_span, col_span, Qt.AlignHCenter)
    return button


def addCheckBox(layout: QGridLayout, text, group, row, col, row_span=1, col_span=1, checked=True):
    checkbox = QCheckBox(text)
    checkbox.setChecked(checked)
    group.addButton(checkbox)
    layout.addWidget(checkbox, row, col, row_span, col_span, Qt.AlignLeft)
    return checkbox


class DailyWidget(QWidget):
    def __init__(self, action_daily: Daily):
        super().__init__()
        self.text_label = action_daily.text_label
        self.action_daily = action_daily
        # self.setFixedSize(272, 467)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.label1 = QLabel("任务选取")
        self.group1 = QButtonGroup()
        self.area1()

        self.label2 = QLabel("练习室类型")
        self.group2 = QButtonGroup()
        self.area2()

        self.label3 = QLabel("练习室难度")
        self.group3 = QButtonGroup()
        self.area3()

        self.label4 = QLabel("购买物品")
        self.group4 = QButtonGroup()
        self.area4()

        self.button_start = addButton(self.layout, "开始", self.handleDailyBtn1, self.layout.rowCount(), 1, 1, 3)
        self.button_stop = addButton(self.layout, "终止", self.handleDailyBtn2, self.layout.rowCount() - 1, 4, 1, 3)

        self.setLayout(self.layout)

        self.action_daily.finished.connect(self.handleFinished)

    def updateDaily(self, action_daily: Daily):
        self.action_daily = action_daily

    def area1(self):
        self.label1.setFixedSize(272, 30)
        # self.label1.setStyleSheet("border-top: 1px solid #D3D3D3;")
        self.group1.setExclusive(False)
        self.layout.addWidget(self.label1, self.layout.rowCount() - 1, 1, 1, 6)
        addCheckBox(self.layout, "训练室任务", self.group1, self.layout.rowCount(), 1, 1, 3)
        addCheckBox(self.layout, "工会支援", self.group1, self.layout.rowCount() - 1, 4, 1, 3)
        addCheckBox(self.layout, "探索回收", self.group1, self.layout.rowCount(), 1, 1, 3)
        addCheckBox(self.layout, "金币商店购买", self.group1, self.layout.rowCount() - 1, 4, 1, 3)

    def area2(self):
        self.label2.setFixedSize(272, 30)
        self.label2.setStyleSheet("border-top: 1px solid #D3D3D3;")
        self.group2.setExclusive(False)
        self.layout.addWidget(self.label2, self.layout.rowCount(), 1, 1, 6)
        addCheckBox(self.layout, "金币收集", self.group2, self.layout.rowCount(), 1, 1, 3, checked=False)
        addCheckBox(self.layout, "魂友育成", self.group2, self.layout.rowCount() - 1, 4, 1, 3)
        addCheckBox(self.layout, "神器育成", self.group2, self.layout.rowCount(), 1, 1, 3, checked=False)
        addCheckBox(self.layout, "武器育成", self.group2, self.layout.rowCount() - 1, 4, 1, 3)

    def area3(self):
        self.label3.setFixedSize(272, 30)
        self.label3.setStyleSheet("border-top: 1px solid #D3D3D3;")
        self.layout.addWidget(self.label3, self.layout.rowCount(), 1, 1, 6)
        addCheckBox(self.layout, "extra", self.group3, self.layout.rowCount(), 1, 1, 2)
        addCheckBox(self.layout, "hard", self.group3, self.layout.rowCount() - 1, 3, 1, 2, checked=False)
        addCheckBox(self.layout, "easy", self.group3, self.layout.rowCount() - 1, 5, 1, 2, checked=False)

    def area4(self):
        self.label4.setFixedSize(272, 30)
        self.label4.setStyleSheet("border-top: 1px solid #D3D3D3;")
        self.group4.setExclusive(False)
        self.layout.addWidget(self.label4, self.layout.rowCount(), 1, 1, 6)
        addCheckBox(self.layout, "SR魂友钥匙", self.group4, self.layout.rowCount(), 1, 1, 2, checked=False)
        addCheckBox(self.layout, "R魂友钥匙", self.group4, self.layout.rowCount() - 1, 3, 1, 2, checked=False)
        addCheckBox(self.layout, "AP体力", self.group4, self.layout.rowCount() - 1, 5, 1, 2)
        addCheckBox(self.layout, "魂友经验", self.group4, self.layout.rowCount(), 1, 1, 2, checked=False)
        addCheckBox(self.layout, "神器经验", self.group4, self.layout.rowCount() - 1, 3, 1, 2, checked=False)
        addCheckBox(self.layout, "武器经验", self.group4, self.layout.rowCount() - 1, 5, 1, 2, checked=False)

    def getNeeds(self):
        needs = [checkbox.isChecked() for checkbox in self.group1.buttons()]
        needs = [i for i, value in enumerate(needs) if value]
        rooms = [checkbox.isChecked() for checkbox in self.group2.buttons()]
        rooms = [i for i, value in enumerate(rooms) if value]
        index = [checkbox.isChecked() for checkbox in self.group3.buttons()].index(True)
        types = [checkbox.isChecked() for checkbox in self.group4.buttons()]
        types = [i for i, value in enumerate(types) if value]
        self.action_daily.getNeeds(needs, rooms, index, types)

    def handleDailyBtn1(self):
        self.getNeeds()
        self.button_start.setDisabled(True)
        self.button_stop.setDisabled(False)
        self.action_daily.start()

    def handleDailyBtn2(self):
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)
        self.action_daily.terminate()
        self.action_daily = Daily(self.action_daily.zoom_factor, self.action_daily.game_area, self.text_label)
        self.action_daily.print("终止操作")

    def handleFinished(self):
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)


class RaidWidget(QWidget):
    def __init__(self, action_raid: Riad):
        super().__init__()
        self.text_label = action_raid.text_label
        self.action_raid = action_raid
        # self.setFixedSize(272, 467)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.label1 = QLabel("任务选取")
        self.group1 = QButtonGroup()
        self.area1()

        self.label2 = QLabel("召唤难度")
        self.group2 = QButtonGroup()
        self.area2()

        self.button_start = addButton(self.layout, "开始", self.handleRaidBtn1, self.layout.rowCount(), 1, 1, 3)
        self.button_stop = addButton(self.layout, "终止", self.handleRaidBtn2, self.layout.rowCount() - 1, 4, 1, 3)

        self.setLayout(self.layout)

        self.action_raid.finished.connect(self.handleFinished)

    def updateRaid(self, action_raid: Riad):
        self.action_raid = action_raid

    def area1(self):
        self.label1.setFixedSize(272, 30)
        # self.label1.setStyleSheet("border-top: 1px solid #D3D3D3;")
        # self.group1.setExclusive(False)
        self.layout.addWidget(self.label1, self.layout.rowCount() - 1, 1, 1, 6)
        addCheckBox(self.layout, "活动任务", self.group1, self.layout.rowCount(), 1, 1, 3, checked=False)
        addCheckBox(self.layout, "raid救援", self.group1, self.layout.rowCount() - 1, 4, 1, 3, checked=False)
        addCheckBox(self.layout, "raid召唤", self.group1, self.layout.rowCount(), 1, 1, 3, checked=False)
        addCheckBox(self.layout, "box扭蛋", self.group1, self.layout.rowCount() - 1, 4, 1, 3, checked=False)

    def area2(self):
        self.label2.setFixedSize(272, 30)
        self.label2.setStyleSheet("border-top: 1px solid #D3D3D3;")
        # self.group1.setExclusive(False)
        self.layout.addWidget(self.label2, self.layout.rowCount(), 1, 1, 6)
        addCheckBox(self.layout, "hell", self.group2, self.layout.rowCount(), 1, 1, 2, checked=False)
        addCheckBox(self.layout, "extra", self.group2, self.layout.rowCount() - 1, 3, 1, 2)
        addCheckBox(self.layout, "hard", self.group2, self.layout.rowCount() - 1, 5, 1, 2, checked=False)

    def getNeeds(self):
        needs = [checkbox.isChecked() for checkbox in self.group1.buttons()]
        needs = [i for i, value in enumerate(needs) if value]
        index = [checkbox.isChecked() for checkbox in self.group2.buttons()].index(True)
        # index = [i for i, value in enumerate(index) if value]
        self.action_raid.getNeeds(needs, index)

    def handleRaidBtn1(self):
        self.getNeeds()
        self.button_start.setDisabled(True)
        self.button_stop.setDisabled(False)
        self.action_raid.start()

    def handleRaidBtn2(self):
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)
        self.action_raid.terminate()
        self.action_raid = Riad(self.action_raid.daily)
        self.action_raid.print("终止操作")

    def handleFinished(self):
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)


class TestWidget(QWidget):
    def __init__(self, zoom_factor: float, game_area: tuple, text_label, action_daily: Daily):
        super().__init__()
        self.zoomFactor = zoom_factor
        self.game_area = game_area
        self.text_label = text_label
        self.action_daily = action_daily

        # self.setFixedSize(272, 467)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 5, 5, 5)

        addButton(self.layout, "点击测试", self.handleDailyBtn1, self.layout.rowCount(), 1, 1, 1)
        addButton(self.layout, "区域测试", self.handleDailyBtn2, self.layout.rowCount(), 1, 1, 1)
        self.setLayout(self.layout)

    def updateDaily(self, action_daily: Daily):
        self.action_daily = action_daily
        self.zoomFactor = action_daily.zoom_factor
        self.game_area = action_daily.game_area

    def handleDailyBtn1(self):
        text = self.text_label.toPlainText()
        if not text:
            return
        area = tuple(float(x) for x in text.split(","))
        print(area)
        operate = Operate(self.zoomFactor, self.game_area, self.text_label)
        operate.position_test(area[0], area[1])

    def handleDailyBtn2(self):
        text = self.text_label.toPlainText()
        if not text:
            return
        area = tuple(float(x) for x in text.split(","))
        if len(area) < 4:
            return
        print(area)
        operate = Operate(self.zoomFactor, self.game_area, self.text_label)
        operate.area_test(area)


class Window(QMainWindow):
    def __init__(self, profile_name="default"):
        super().__init__()
        self.setWindowTitle("crave saga")
        self.setGeometry(100, 100, 667, 667)
        self.setMinimumSize(375, 667)

        # 创建浏览器窗口
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # 记录位置
        pos = self.browser.mapToGlobal(self.browser.pos())
        self.game_area = (pos.x(), pos.y(), int(self.browser.height() * 375 / 667), self.browser.height())
        self.zoomFactor = 1

        # 侧边栏文本区域
        self.text_label = QTextEdit(self)
        # self.text_label.setFixedSize(282, 200)
        # self.text_label.setReadOnly(True)
        self.text_label.setStyleSheet("QTextEdit { margin: 5px; }")
        self.tab_widget = QTabWidget(self)

        # 操作对象
        self.action_daily = Daily(self.zoomFactor, self.game_area, self.text_label)
        self.action_raid = Riad(self.action_daily)

        # 创建侧边栏 QDockWidget
        self.sidebar = QDockWidget(self)
        self.sidebar.setFeatures(QDockWidget.NoDockWidgetFeatures)  # 设置侧边栏不可移动
        self.sidebar.setTitleBarWidget(QWidget())  # 隐藏标题栏
        self.sidebar.setHidden(True)  # 默认隐藏
        self.sidebarIsVisible = False

        # 侧边栏
        self.side_widget = QWidget(self)
        self.side_layout = QVBoxLayout()
        self.side_layout.setContentsMargins(0, 5, 0, 0)
        self.side_widget.setStyleSheet("QWidget { background-color: #F5F5F5 }")

        # 每日任务选项卡
        self.daily_widget = DailyWidget(self.action_daily)
        self.tab_widget.addTab(self.daily_widget, '日常任务')

        # Riad选项卡
        self.raid_widget = RaidWidget(self.action_raid)
        self.tab_widget.addTab(self.raid_widget, 'Raid/无限池')

        # 测试选项卡
        self.test_widget = TestWidget(self.zoomFactor, self.game_area, self.text_label, self.action_daily)
        self.tab_widget.addTab(self.test_widget, '测试')

        # 添加各区域到侧边栏
        self.side_layout.addWidget(self.tab_widget)
        self.side_layout.addWidget(self.text_label)
        self.side_widget.setLayout(self.side_layout)

        self.sidebar.setWidget(self.side_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.sidebar)

        # 初始化浏览器
        self.initBrowser(profile_name)

        # 初始化右键菜单动作
        self.reload_action = QAction('重新加载', self)
        self.reload_action.triggered.connect(self.browser.reload)

        self.toggle_sidebar_action = QAction('显示侧边栏', self)
        self.toggle_sidebar_action.setCheckable(True)
        self.toggle_sidebar_action.setChecked(True)
        self.toggle_sidebar_action.triggered.connect(self.sidebarToggle)

        self.web_mute_action = QAction('静音', self)
        self.web_mute_action.setCheckable(True)
        self.web_mute_action.setChecked(False)
        self.web_mute_action.triggered.connect(self.webMute)

    def initBrowser(self, profile_name):
        # 确保缓存路径存在
        current_dir = os.path.dirname(os.path.abspath(__file__))
        common_cache_path = os.path.join(current_dir, "cache", "common")  # 公共缓存路径
        individual_profile_path = os.path.join(current_dir, "cache", profile_name)  # 每个profile的独立路径
        os.makedirs(common_cache_path, exist_ok=True)
        os.makedirs(individual_profile_path, exist_ok=True)

        # 缓存设置
        profile = QWebEngineProfile(profile_name, self)
        profile.setCachePath(common_cache_path)
        profile.setPersistentStoragePath(individual_profile_path)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        # 加载网页
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)
        self.browser.setPage(QWebEnginePage(profile, self.browser))
        self.browser.loadFinished.connect(self.handleFirstLoadFinished)
        self.browser.setUrl(QUrl("https://game.ero-labs.shop/cn/cloud_game.html?id=47&connect_type=1&connection_id=29"))
        # self.browser.setUrl(QUrl("https://www.baidu.com"))
        # self.sidebar.setVisible(True)

    def updatePosition(self):
        self.zoomFactor = self.browser.height() / 667
        pos = self.browser.mapToGlobal(self.browser.pos())
        self.game_area = (pos.x(), pos.y(), int(self.browser.height() * 375 / 667), self.browser.height())

        self.action_daily.update(self.zoomFactor, self.game_area)
        self.action_raid.update(self.action_daily)

        self.daily_widget.updateDaily(self.action_daily)
        self.raid_widget.updateRaid(self.action_raid)
        self.test_widget.updateDaily(self.action_daily)

    def resizeEvent(self, event):
        # 重写调整大小
        new_height = event.size().height()
        new_width = int(new_height * 375 / 667 + 292 * self.sidebarIsVisible)
        self.resize(new_width, new_height)
        super().resizeEvent(event)

    def event(self, event):
        if event.type() == QEvent.Move:
            # 窗口位置发生变化时更新位置
            self.updatePosition()
            print(self.game_area)
        elif event.type() == QEvent.Resize:
            # 窗口大小发生变化时更新大小
            self.browser.resize(self.width(), self.height())
            self.updatePosition()
            self.browser.setZoomFactor(self.zoomFactor)
            print(self.game_area)
        return super().event(event)

    def contextMenuEvent(self, event):
        # 重写右键菜单
        menu = QMenu(self)

        menu.addAction(self.reload_action)
        menu.addAction(self.toggle_sidebar_action)
        menu.addAction(self.web_mute_action)

        menu.exec_(event.globalPos())

    def sidebarToggle(self):
        if self.sidebar.isVisible():
            self.sidebarIsVisible = False
            self.toggle_sidebar_action.setChecked(False)
            self.sidebar.setHidden(True)
            new_height = self.height()
            new_width = int(new_height * 375 / 667)
            self.resize(new_width, new_height)
        else:
            self.sidebarIsVisible = True
            self.toggle_sidebar_action.setChecked(True)
            new_height = self.height()
            new_width = int(new_height * 375 / 667 + 292)
            self.resize(new_width, new_height)
            self.sidebar.setVisible(True)

    def webMute(self):
        self.browser.page().setAudioMuted(not self.browser.page().isAudioMuted())
        self.web_mute_action.setChecked(self.web_mute_action.isChecked())

    def handleFirstLoadFinished(self, ok):
        if ok:
            # 网页加载完成，延迟2秒后执行操作
            QTimer.singleShot(2000, self.getFrame)

    def getFrame(self):
        script = """
            var gameFrame = document.querySelector("#game_frame");
            var src = gameFrame ? gameFrame.src : null;  // 检查gameFrame是否存在
            src;
        """
        self.browser.page().runJavaScript(script, self.loadFrame)

    def loadFrame(self, result):
        # 处理JavaScript代码执行结果
        if isinstance(result, str) and result != "":
            self.browser.loadFinished.connect(self.loadGame)
            self.browser.setUrl(QUrl(result))
        else:
            # 继续获取URL
            QTimer.singleShot(1000, self.getFrame)

    def delayLoadGame(self, ok):
        if ok:
            QTimer.singleShot(1000, self.loadGame)

    def loadGame(self):
        script = """
            var background = document.getElementById('Background');
            background.style.display = 'none';
            var gameDiv = document.getElementById('GameDiv');
            gameDiv.style.position = 'fixed';
            gameDiv.style.top = '0';
            gameDiv.style.left = '0';
        """
        # TODO test -----
        # self.browser.setZoomFactor(1.5)
        # new_height = int(667 * 1.5)
        # new_width = int(667 * 1.5)
        # self.resize(new_width, new_height)
        # self.browser.resize(new_width, new_height)
        # ----

        self.browser.page().runJavaScript(script)
        self.sidebar.setVisible(True)
        self.sidebarIsVisible = True
        self.resize(self.width(), self.height() + 292 * self.sidebarIsVisible)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
