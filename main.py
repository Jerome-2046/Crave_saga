import os
import sys

from PyQt5.QtCore import Qt, QUrl, QTimer, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDockWidget, QPushButton, QTextEdit, QVBoxLayout, \
    QGridLayout, QMenu, QAction, QTabWidget, QCheckBox, QButtonGroup, QLabel


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

        # 初始化浏览器
        self.initBrowser(profile_name)

        # 初始化右键菜单动作
        self.reload_action = QAction('重新加载', self)
        self.reload_action.triggered.connect(self.browser.reload)

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

    def resizeEvent(self, event):
        # 重写调整大小
        new_height = event.size().height()
        new_width = int(new_height * 375 / 667)
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
        menu.addAction(self.web_mute_action)

        menu.exec_(event.globalPos())

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

        self.browser.page().runJavaScript(script)
        self.sidebar.setVisible(True)
        self.resize(self.width(), self.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
