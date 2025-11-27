import os
import random
import sys
import time
from PyQt5.QtCore import QTimer, Qt, QTime, QPoint, QPropertyAnimation, QParallelAnimationGroup, QSequentialAnimationGroup, pyqtProperty
from PyQt5.QtGui import QPainter, QBrush, QPalette, QFont, QColor, QPixmap, QTransform
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtWidgets import (
    QApplication,
    QFontComboBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QWidget,
    QPlainTextEdit,
    QHBoxLayout,
    QGraphicsOpacityEffect
)

class AnimatedDigit(QLabel):
    def __init__(self, parent=None, image_folder="images", size=200, new_digit_space=0.5, old_digit_space=0.5):
        super().__init__(parent)
        self.image_folder = image_folder
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.size = size
        self.new_digit_space = 1 / new_digit_space
        self.old_digit_space = 1 / old_digit_space
        self.setFixedSize(self.size, self.size)
        self.current_digit = 0
        self.original_pixmap = QPixmap(f'{self.image_folder}/digit_{self.current_digit}.png')
        self.setPixmap(self.original_pixmap)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1)
        self._scale_factor = 1.0
        self.is_animating = False

    def set_digit(self, digit):
        self.current_digit = digit
        self.original_pixmap = QPixmap(f'{self.image_folder}/digit_{self.current_digit}.png')
        self.setPixmap(self.original_pixmap)

    def set_animation_digit_space(self, new_digit_space=0.5, old_digit_space=0.5):
        self.new_digit_space = 1 / new_digit_space
        self.old_digit_space = 1 / old_digit_space

    def set_size(self, size):
        self.size = size
        self.setFixedSize(self.size, self.size)

    def animate_digit_change(self, new_digit):
        if self.current_digit == new_digit:
            return

        self.new_digit_label = QLabel(self.parent())
        self.new_digit_label.setPixmap(QPixmap(f'{self.image_folder}/digit_{new_digit}.png'))
        self.new_digit_label.setAlignment(Qt.AlignCenter)
        self.new_digit_label.setScaledContents(True)
        self.new_digit_label.setFixedSize(self.size, self.size)
        self.new_digit_label.move(self.x(), self.y() - self.height() / self.new_digit_space)

        new_opacity_effect = QGraphicsOpacityEffect(self.new_digit_label)
        self.new_digit_label.setGraphicsEffect(new_opacity_effect)
        new_opacity_animation = QPropertyAnimation(new_opacity_effect, b"opacity")
        new_opacity_animation.setDuration(500)
        new_opacity_animation.setStartValue(0)
        if self.new_digit_space < 0.6:
            new_opacity_animation.setKeyValueAt(0.3, 0.6)
        new_opacity_animation.setEndValue(1)

        self.new_digit_label.show()

        self.new_digit_animation = QPropertyAnimation(self.new_digit_label, b"pos")
        self.new_digit_animation.setDuration(500)
        self.new_digit_animation.setStartValue(QPoint(self.x(), self.y() - self.height() / self.new_digit_space))
        self.new_digit_animation.setEndValue(self.pos())

        self.old_digit_animation = QPropertyAnimation(self, b"pos")
        self.old_digit_animation.setDuration(500)
        self.old_digit_animation.setStartValue(self.pos())
        self.old_digit_animation.setEndValue(QPoint(self.x(), self.y() + self.height() / self.old_digit_space))

        old_opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        old_opacity_animation.setDuration(500)
        old_opacity_animation.setStartValue(1)
        old_opacity_animation.setEndValue(0)

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.new_digit_animation)
        self.animation_group.addAnimation(self.old_digit_animation)
        self.animation_group.addAnimation(old_opacity_animation)
        self.animation_group.addAnimation(new_opacity_animation)
        self.animation_group.finished.connect(lambda: self.update_digit(new_digit))

        self.animation_group.start()

    def update_digit(self, new_digit):
        self.set_digit(new_digit)
        self.new_digit_label.deleteLater()
        self.move(self.x(), self.y() - self.height() / self.old_digit_space)
        self.opacity_effect.setOpacity(1)

    def setup_animations(self):
        self.initial_scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.initial_scale_animation.setDuration(500)
        self.initial_scale_animation.setStartValue(1.0)
        self.initial_scale_animation.setEndValue(1.1)

        self.scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation.setDuration(1000)
        self.scale_animation.setStartValue(1.1)
        self.scale_animation.setEndValue(0.9)

        self.scale_animation_reverse = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation_reverse.setDuration(1000)
        self.scale_animation_reverse.setStartValue(0.9)
        self.scale_animation_reverse.setEndValue(1.1)

        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.5)

        self.opacity_animation_reverse = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation_reverse.setDuration(1000)
        self.opacity_animation_reverse.setStartValue(0.5)
        self.opacity_animation_reverse.setEndValue(1.0)

        self.pulsing_animation_group = QParallelAnimationGroup()
        self.pulsing_animation_group.addAnimation(self.scale_animation)
        self.pulsing_animation_group.addAnimation(self.opacity_animation)

        self.reverse_animation_group = QParallelAnimationGroup()
        self.reverse_animation_group.addAnimation(self.scale_animation_reverse)
        self.reverse_animation_group.addAnimation(self.opacity_animation_reverse)

        self.full_animation_group = QSequentialAnimationGroup()
        self.full_animation_group.addAnimation(self.pulsing_animation_group)
        self.full_animation_group.addAnimation(self.reverse_animation_group)

    def animate_pulsing(self, t_start):
        self.is_animating = True
        self.setup_animations()
        QTimer.singleShot(t_start, self.initial_scale_animation.start)
        self.initial_scale_animation.finished.connect(self.start_looping_animation)

    def start_looping_animation(self):
        self.full_animation_group.setLoopCount(-1)
        self.full_animation_group.start()

    def stop_animation(self):
        if hasattr(self, 'full_animation_group'):
            self.full_animation_group.stop()
        self.is_animating = False
        self.scale_factor = 1.0
        self.update()
        self.opacity_effect.setOpacity(1)

    @pyqtProperty(float)
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, factor):
        self._scale_factor = factor
        self.update()

    def paintEvent(self, event):
        if self.is_animating:
            painter = QPainter(self)
            scaled_pixmap = self.original_pixmap.scaled(self.size * self._scale_factor, self.size * self._scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled_pixmap.width()) / 2
            y = (self.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            super().paintEvent(event)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.high = self.height() * 1.5

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(Qt.black))
        self.scene.setSceneRect(0, 0, self.high, self.high)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.scene.setPalette(p)
        self.setPalette(p)

        self.view = QGraphicsView()
        self.view.setFixedHeight(self.high)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setStyleSheet("border: 0px")
        self.view.setRenderHint(QPainter.HighQualityAntialiasing)
        self.view.setScene(self.scene)

        self.main_layout = QVBoxLayout()
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.view)

        self.digit_container = QWidget()
        self.digit_container.setFixedHeight(400)
        self.digit_layout = QHBoxLayout(self.digit_container)
        self.digit_layout.setContentsMargins(0, 80, 0, 0)
        self.digit_layout.setSpacing(0)
        self.digit_layout.setAlignment(Qt.AlignCenter)

        if hasattr(sys, '_MEIPASS'):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.abspath(".")

        self.minute_tens = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_white"), new_digit_space=0.8)
        self.minute_units = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_white"), size=170, new_digit_space=0.3)
        self.second_tens = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_grey"), size=170, new_digit_space=0.3)
        self.second_units = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_grey"), new_digit_space=0.8)

        self.digit_layout.addWidget(self.minute_tens)
        self.digit_layout.addWidget(self.minute_units)
        self.colon_label = QLabel(":")
        self.colon_label.setAlignment(Qt.AlignCenter)
        self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
        self.digit_layout.addWidget(self.colon_label)
        self.digit_layout.addWidget(self.second_tens)
        self.digit_layout.addWidget(self.second_units)

        self.main_layout.addWidget(self.digit_container, alignment=Qt.AlignCenter)

        self.label2 = QLabel('', alignment=Qt.AlignHCenter)
        p.setColor(QPalette.WindowText, Qt.white)
        self.label2.setPalette(p)
        self.font = QFont('Arial', 80)
        self.label2.setFont(self.font)
        self.label2.setWordWrap(True)
        self.label2.setHidden(True)
        self.main_layout.addWidget(self.label2)
        self.setLayout(self.main_layout)

        self.rb0 = QSvgWidget()
        self.rb0.setFixedSize(self.high, self.high)
        self.rb0.load(os.path.join(basedir, 'деления_и_цифры.svg'))
        self.scene.addWidget(self.rb0)

        renderer = QSvgRenderer(os.path.join(basedir, "hour_arrow.svg"))
        self.rb01 = QGraphicsSvgItem()
        self.rb01.setSharedRenderer(renderer)
        self.rb01.setScale(self.high / 543)
        transX0 = self.rb01.boundingRect().width() * 0.5
        transY0 = self.rb01.boundingRect().height() - self.rb01.boundingRect().width() * 0.5
        transX = self.high * (21 / 543)
        transY = self.high * (152 / 543)
        self.rb01.setTransformOriginPoint(transX0, transY0)
        deltaX = transX - transX0
        deltaY = transY - transY0
        self.rb01.setX(self.high * (0.5 - 21 / 543) + deltaX)
        self.rb01.setY(self.high * (0.5 - 152 / 543) + deltaY)
        self.rb01.setRotation(random.uniform(0, 360))
        self.scene.addItem(self.rb01)

        renderer2 = QSvgRenderer(os.path.join(basedir, "минутная_стрелка.svg"))
        self.rb02 = QGraphicsSvgItem()
        self.rb02.setSharedRenderer(renderer2)
        self.rb02.setScale(self.high / 543)
        transX02 = self.rb02.boundingRect().width() * 0.5
        transY02 = self.rb02.boundingRect().height() - self.rb02.boundingRect().width() * 0.5
        transX2 = self.high * (21 / 543)
        transY2 = self.high * (245 / 543)
        self.rb02.setTransformOriginPoint(transX02, transY02)
        deltaX2 = transX2 - transX02
        deltaY2 = transY2 - transY02
        self.rb02.setX(self.high * (0.5 - 21 / 543) + deltaX2)
        self.rb02.setY(self.high * (0.5 - 245 / 543) + deltaY2)
        self.rb02.setRotation(random.uniform(0, 360) - 0.2)
        self.scene.addItem(self.rb02)

        renderer3 = QSvgRenderer(os.path.join(basedir, "секундная_стрелка.svg"))
        self.rb03 = QGraphicsSvgItem()
        self.rb03.setSharedRenderer(renderer3)
        self.rb03.setScale(0.25 * self.high / 543)
        transX03 = self.rb03.boundingRect().width() * 0.5
        transY03 = self.rb03.boundingRect().height() - self.rb03.boundingRect().width() * 4
        transX3 = self.high * (transX03 / 543)
        transY3 = self.high * (transY03 / 543)
        self.rb03.setTransformOriginPoint(transX03, transY03)
        deltaX3 = transX3 - transX03
        deltaY3 = transY3 - transY03
        self.rb03.setX(self.high * (0.5 - transX03 / 543) + deltaX3)
        self.rb03.setY(self.high * (0.5 - transY03 / 543) + deltaY3)
        self.rb03.setRotation(360 * 30 / 60)
        self.scene.addItem(self.rb03)

        self.second = int(time.strftime('%S'))
        self.start_minute = int(time.strftime('%M'))
        self.start_hour = int(time.strftime('%H'))

        self.countdown_minute = 1
        self.countdown_second = 0
        self.countdownEvent = False
        self.flickNum = 7

        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate1deg)
        self.timer.start(1000)
        self.stopCountDown()

    def changeClockDivisions(self, high):
        self.rb0.setFixedSize(high, high)

    def changeHourArrow(self, high):
        self.rb01.setScale(high / 543)
        transX0 = self.rb01.boundingRect().width() * 0.5
        transY0 = self.rb01.boundingRect().height() - self.rb01.boundingRect().width() * 0.5
        transX = high * (21 / 543)
        transY = high * (152 / 543)
        self.rb01.setTransformOriginPoint(transX0, transY0)
        deltaX = transX - transX0
        deltaY = transY - transY0
        self.rb01.setX(high * (0.5 - 21 / 543) + deltaX)
        self.rb01.setY(high * (0.5 - 152 / 543) + deltaY)

    def changeMinuteArrow(self, high):
        self.rb02.setScale(high / 543)
        transX02 = self.rb02.boundingRect().width() * 0.5
        transY02 = self.rb02.boundingRect().height() - self.rb02.boundingRect().width() * 0.5
        transX2 = high * (21 / 543)
        transY2 = high * (245 / 543)
        self.rb02.setTransformOriginPoint(transX02, transY02)
        deltaX2 = transX2 - transX02
        deltaY2 = transY2 - transY02
        self.rb02.setX(high * (0.5 - 21 / 543) + deltaX2)
        self.rb02.setY(high * (0.5 - 245 / 543) + deltaY2)

    def changeSecondArrow(self, high):
        self.rb03.setScale(0.25 * high / 543)
        transX03 = self.rb03.boundingRect().width() * 0.5
        transY03 = self.rb03.boundingRect().height() - self.rb03.boundingRect().width() * 4
        transX3 = high * (transX03 / 543)
        transY3 = high * (transY03 / 543)
        self.rb03.setTransformOriginPoint(transX03, transY03)
        deltaX3 = transX3 - transX03
        deltaY3 = transY3 - transY03
        self.rb03.setX(high * (0.5 - transX03 / 543) + deltaX3)
        self.rb03.setY(high * (0.5 - transY03 / 543) + deltaY3)

    def changeClock(self, high):
        self.scene.setSceneRect(0, 0, high, high)
        self.changeClockDivisions(high)
        self.changeHourArrow(high)
        self.changeMinuteArrow(high)
        self.changeSecondArrow(high)

    def rotate1deg(self):
        self.second = (self.second + 1) % 60
        self.rb03.setRotation(360 * int(time.strftime('%S')) / 60)
        self.rb02.setRotation(360 * (int(time.strftime('%M')) + int(time.strftime('%S')) / 60) / 60)
        self.rb01.setRotation(360 * (int(time.strftime('%H')) + int(time.strftime('%M')) / 60 + (int(time.strftime('%S')) / 60) / 60) / 12)
        self.scene.update()
        if self.countdownEvent:
            self.countdown()

    def startCountDown(self, minutes, seconds):
        self.countdown_minute = minutes
        self.countdown_second = seconds
        self.countdownEvent = True
        self.flickNum = 7
        self.view.setFixedHeight(self.high / 1.3)
        self.changeClock(self.high / 1.4)
        self.digit_container.setVisible(True)
        self.timer.start(1000)

    def stopCountDown(self):
        self.countdownEvent = False
        self.digit_container.setVisible(False)
        self.minute_tens.stop_animation()
        self.minute_units.stop_animation()
        self.second_tens.stop_animation()
        self.second_units.stop_animation()
        self.scene.setBackgroundBrush(QBrush(Qt.black))
        self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.scene.setPalette(p)
        self.setPalette(p)
        self.changeClock(self.high)
        self.view.setFixedHeight(self.high)
        self.view.setAlignment(Qt.AlignHCenter)

    def countdown(self):
        if self.countdown_minute == 0 and self.countdown_second == 0:
            self.timer.stop()
            return
        if self.countdown_second == 0:
            self.countdown_minute -= 1
            self.countdown_second = 59
        else:
            self.countdown_second -= 1
        if self.countdown_minute == 0 and self.countdown_second < 6:
            self.flick()
        self.minute_tens.animate_digit_change(self.countdown_minute // 10)
        self.minute_units.animate_digit_change(self.countdown_minute % 10)
        self.second_tens.animate_digit_change(self.countdown_second // 10)
        self.second_units.animate_digit_change(self.countdown_second % 10)

    def flick(self):
        if self.flickNum % 2 == 1 and self.flickNum > 1:
            self.scene.setBackgroundBrush(QBrush(Qt.black))
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.black)
            self.scene.setPalette(p)
            self.setPalette(p)
            self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
            self.flickNum -= 1
        elif self.flickNum > 1:
            dark_red = QColor(139, 0, 0)
            self.scene.setBackgroundBrush(QBrush(dark_red))
            p = self.palette()
            p.setColor(self.backgroundRole(), dark_red)
            self.scene.setPalette(p)
            self.setPalette(p)
            self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: rgb(139, 0, 0);")
            self.flickNum -= 1
            if self.flickNum == 1:
                self.minute_tens.animate_pulsing(1000)
                self.minute_units.animate_pulsing(1500)
                self.second_tens.animate_pulsing(2000)
                self.second_units.animate_pulsing(2500)

    def drawText(self, text):
        self.view.setHidden(True)
        self.label2.setText(text)
        self.label2.setHidden(False)

    def hideText(self):
        self.view.setHidden(False)
        self.label2.setHidden(True)

class PreviewWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.window = main_window.window
        self.high = 200  # Фиксированный размер мини-копии

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(Qt.black))
        self.scene.setSceneRect(0, 0, self.high, self.high)
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(self.high, self.high)
        self.view.setStyleSheet("border: 0px")
        self.view.setRenderHint(QPainter.HighQualityAntialiasing)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)

        if hasattr(sys, '_MEIPASS'):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.abspath(".")

        self.clock_item = QGraphicsSvgItem(os.path.join(basedir, "деления_и_цифры.svg"))
        self.clock_item.setScale(self.high / 543)
        self.scene.addItem(self.clock_item)

        self.hour_hand = QGraphicsSvgItem(os.path.join(basedir, "hour_arrow.svg"))
        self.hour_hand.setScale(self.high / 543)
        self.set_hand_position(self.hour_hand, 21 / 543, 152 / 543)
        self.scene.addItem(self.hour_hand)

        self.minute_hand = QGraphicsSvgItem(os.path.join(basedir, "минутная_стрелка.svg"))
        self.minute_hand.setScale(self.high / 543)
        self.set_hand_position(self.minute_hand, 21 / 543, 245 / 543)
        self.scene.addItem(self.minute_hand)

        self.second_hand = QGraphicsSvgItem(os.path.join(basedir, "секундная_стрелка.svg"))
        self.second_hand.setScale(0.25 * self.high / 543)
        self.set_hand_position(self.second_hand, self.second_hand.boundingRect().width() / 543,
                              (self.second_hand.boundingRect().height() - self.second_hand.boundingRect().width() * 4) / 543)
        self.scene.addItem(self.second_hand)

        self.digit_container = QWidget()
        self.digit_layout = QHBoxLayout(self.digit_container)
        self.digit_layout.setContentsMargins(0, 0, 0, 0)
        self.digit_layout.setSpacing(0)

        self.minute_tens = AnimatedDigit(self, os.path.join(basedir, "images_white"), size=50, new_digit_space=0.8, old_digit_space=0.8)
        self.minute_units = AnimatedDigit(self, os.path.join(basedir, "images_white"), size=50, new_digit_space=0.3, old_digit_space=0.3)
        self.colon_label = QLabel(":")
        self.colon_label.setStyleSheet("color: white; font-size: 50px; background-color: black;")
        self.second_tens = AnimatedDigit(self, os.path.join(basedir, "images_grey"), size=50, new_digit_space=0.3, old_digit_space=0.3)
        self.second_units = AnimatedDigit(self, os.path.join(basedir, "images_grey"), size=50, new_digit_space=0.8, old_digit_space=0.8)

        self.digit_layout.addWidget(self.minute_tens)
        self.digit_layout.addWidget(self.minute_units)
        self.digit_layout.addWidget(self.colon_label)
        self.digit_layout.addWidget(self.second_tens)
        self.digit_layout.addWidget(self.second_units)
        self.layout.addWidget(self.digit_container)

        self.text_label = QLabel("Текст отображен", alignment=Qt.AlignHCenter)
        self.text_label.setStyleSheet("color: white; font-size: 20px; background-color: black;")
        self.text_label.setHidden(True)
        self.layout.addWidget(self.text_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(1000)

    def set_hand_position(self, hand, x_ratio, y_ratio):
        transX0 = hand.boundingRect().width() * 0.5
        transY0 = hand.boundingRect().height() - hand.boundingRect().width() * 0.5
        transX = self.high * x_ratio
        transY = self.high * y_ratio
        hand.setTransformOriginPoint(transX0, transY0)
        deltaX = transX - transX0
        deltaY = transY - transY0
        hand.setPos(self.high * (0.5 - x_ratio) + deltaX, self.high * (0.5 - y_ratio) + deltaY)

    def update_preview(self):
        self.hour_hand.setRotation(self.window.rb01.rotation())
        self.minute_hand.setRotation(self.window.rb02.rotation())
        self.second_hand.setRotation(self.window.rb03.rotation())

        if self.window.countdownEvent:
            self.digit_container.setVisible(True)
            self.minute_tens.animate_digit_change(self.window.countdown_minute // 10)
            self.minute_units.animate_digit_change(self.window.countdown_minute % 10)
            self.second_tens.animate_digit_change(self.window.countdown_second // 10)
            self.second_units.animate_digit_change(self.window.countdown_second % 10)
            if self.window.countdown_minute == 0 and self.window.countdown_second < 6:
                self.scene.setBackgroundBrush(QBrush(Qt.black if self.window.flickNum % 2 == 1 else QColor(139, 0, 0)))
                self.colon_label.setStyleSheet(f"color: white; font-size: 50px; background-color: {'black' if self.window.flickNum % 2 == 1 else 'rgb(139, 0, 0)'};")
            if self.window.countdown_minute == 0 and self.window.countdown_second == 0:
                self.minute_tens.animate_pulsing(1000)
                self.minute_units.animate_pulsing(1500)
                self.second_tens.animate_pulsing(2000)
                self.second_units.animate_pulsing(2500)
        else:
            self.digit_container.setVisible(False)

        if not self.window.label2.isHidden():
            self.text_label.setHidden(False)
            self.view.setHidden(True)
        else:
            self.text_label.setHidden(True)
            self.view.setHidden(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clock Control Panel")
        self.window = Window()
        self.window.setMinimumSize(543, 543)
        self.window.show()

        layout = QVBoxLayout()
        self.button = QPushButton('Спрятать часы')
        layout.addWidget(self.button)

        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        self.timeEdit.setTime(QTime(0, 5, 0))
        layout.addWidget(self.timeEdit)

        self.button1 = QPushButton('Включить обратный отсчет')
        layout.addWidget(self.button1)

        self.fontBox = QFontComboBox()
        layout.addWidget(self.fontBox)

        self.textEdit = QPlainTextEdit()
        layout.addWidget(self.textEdit)

        self.button2 = QPushButton('Отобразить текст')
        layout.addWidget(self.button2)

        self.preview_widget = PreviewWidget(self)
        self.preview_widget.setHidden(True)
        layout.addWidget(self.preview_widget)

        self.preview_button = QPushButton("Показать превью")
        self.preview_button.clicked.connect(self.toggle_preview)
        layout.addWidget(self.preview_button)

        widget = QWidget()
        widget.setLayout(layout)

        self.button.clicked.connect(self.on_click1)
        self.button1.clicked.connect(self.on_click2)
        self.button2.clicked.connect(self.on_click3)
        self.textEdit.textChanged.connect(self.on_click3_change)
        self.fontBox.currentFontChanged.connect(self.onFontChanged)

        self.setCentralWidget(widget)

    def on_click1(self):
        if self.button.text() == 'Отобразить часы':
            self.window.view.setHidden(False)
            self.window.digit_container.setFixedHeight(400)
            self.window.minute_tens.set_size(200)
            self.window.minute_tens.set_animation_digit_space(new_digit_space=0.8)
            self.window.minute_units.set_size(170)
            self.window.minute_units.set_animation_digit_space(new_digit_space=0.3)
            self.window.second_tens.set_size(170)
            self.window.second_tens.set_animation_digit_space(new_digit_space=0.3)
            self.window.second_units.set_size(200)
            self.window.second_units.set_animation_digit_space(new_digit_space=0.8)
            self.button.setText('Спрятать часы')
        else:
            self.window.view.setHidden(True)
            self.window.digit_container.setFixedHeight(600)
            self.window.minute_tens.set_size(250)
            self.window.minute_tens.set_animation_digit_space(new_digit_space=0.8, old_digit_space=0.8)
            self.window.minute_units.set_size(250)
            self.window.minute_units.set_animation_digit_space(new_digit_space=0.8, old_digit_space=0.8)
            self.window.second_tens.set_size(250)
            self.window.second_tens.set_animation_digit_space(new_digit_space=0.8, old_digit_space=0.8)
            self.window.second_units.set_size(250)
            self.window.second_units.set_animation_digit_space(new_digit_space=0.8, old_digit_space=0.8)
            self.button.setText('Отобразить часы')

    def on_click2(self):
        if self.button1.text() == 'Включить обратный отсчет':
            self.window.startCountDown(self.timeEdit.time().hour() * 60 + self.timeEdit.time().minute(), self.timeEdit.time().second())
            self.button1.setText('Выключить обратный отсчет')
        else:
            self.window.stopCountDown()
            self.button1.setText('Включить обратный отсчет')

    def on_click3(self):
        if self.button2.text() == 'Отобразить текст':
            self.window.drawText(self.textEdit.toPlainText())
            self.button2.setText('Скрыть текст')
        else:
            self.window.hideText()
            self.button2.setText('Отобразить текст')

    def on_click3_change(self):
        if self.button2.text() == 'Скрыть текст':
            self.window.drawText(self.textEdit.toPlainText())

    def onFontChanged(self):
        custom_font = self.fontBox.currentFont()
        custom_font.setPixelSize(80)
        self.window.label2.setFont(custom_font)

    def toggle_preview(self):
        if self.preview_widget.isHidden():
            self.preview_widget.setHidden(False)
            self.preview_button.setText("Скрыть превью")
        else:
            self.preview_widget.setHidden(True)
            self.preview_button.setText("Показать превью")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())