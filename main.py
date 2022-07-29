import os

from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import uic

class videoPlayer:
    def __init__(self):
        # 初始化
        self.ui = uic.loadUi('./video.ui')  # 加载designer设计的ui程序
        # 播放器
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.ui.wgt_player)

        # 按钮
        self.ui.btn_select.clicked.connect(self.open)
        self.ui.btn_play_pause.clicked.connect(self.playPause)
        self.ui.imge.setStyleSheet("image: url(./volume.png)")
        self.ui.btn_play_pause.setStyleSheet("border:none;"
                                             "image: url(./start.png)")
        # 进度条
        self.player.durationChanged.connect(self.getDuration)
        self.player.positionChanged.connect(self.getPosition)
        self.ui.sld_duration.sliderMoved.connect(self.updatePosition)
        self.ui.volumeSlider.valueChanged.connect(self.set_volume_func)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.playPause()

    def set_volume_func(self):
        self.player.setVolume(self.ui.volumeSlider.value())


    # 打开视频文件
    def open(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
        self.player.play()
    # 播放视频
    def playPause(self):
        if self.player.state()==1:
            self.ui.btn_play_pause.setStyleSheet("border:none;"
                                                 "image: url(./start.png)")
            self.player.pause()
        else:
            self.ui.btn_play_pause.setStyleSheet("border:none;"
                                                 "image: url(./stop.png)")
            self.player.play()
    # 视频总时长获取
    def getDuration(self, d):
        '''d是获取到的视频总时长（ms）'''
        self.ui.sld_duration.setRange(0, d)
        self.ui.sld_duration.setEnabled(True)
        self.displayTime(d)
    # 视频实时位置获取
    def getPosition(self, p):
        self.ui.sld_duration.setValue(p)
        self.displayTime(p)
    # 显示剩余时间
    def displayTime(self, ms):
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.ui.lab_duration.setText('{}:{}'.format(minutes, seconds))
    # 用进度条更新视频位置
    def updatePosition(self, v):
        self.player.setPosition(v)
        self.displayTime(self.ui.sld_duration.maximum()-v)

    def updatevld(self, v):
        self.player.setPosition(v)
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.displayTime(self.ui.sld_duration.maximum()-v)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
        self.parent.m_drag = True
        self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos() - self.parent.m_DragPosition)  # move将窗口移动到指定位置
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = False
        self.unsetCursor()
if __name__ == "__main__":
    app = QApplication([])
    myPlayer = videoPlayer()
    myPlayer.ui.show()
    app.exec()
