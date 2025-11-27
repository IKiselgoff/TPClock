"""Главная точка входа: панель управления и окно с часами."""

import os
import random
import sys
import time

from animated_digit import AnimatedDigit
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QColor, QFont, QPalette, QPainter, QBrush
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer, QSvgWidget
from PyQt5.QtWidgets import (
    QApplication,
    QFontComboBox,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Панель оператора для управления вторым окном с часами."""

    def __init__(self):
        super().__init__()

        # --- Настройка вспомогательного окна с часами ---
        self.setWindowTitle("Clock Control Panel")
        self.window = Window()
        self.window.setMinimumSize(543, 543)
        self.window.show()

        # --- Панель управления слева ---
        controls = self._build_controls()
        self._connect_signals()

        widget = QWidget()
        widget.setLayout(controls)
        self.setCentralWidget(widget)

    def _build_controls(self):
        """Собирает панель управления для оператора."""

        layout = QVBoxLayout()

        # --- Управление отображением часов ---
        self.button = QPushButton("Спрятать часы")
        layout.addWidget(self.button)

        # --- Настройка времени обратного отсчёта ---
        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        self.timeEdit.setTime(QTime(0, 5, 0))
        layout.addWidget(self.timeEdit)

        self.button1 = QPushButton("Включить обратный отсчет")
        layout.addWidget(self.button1)

        # --- Управление текстовой заставкой ---
        self.fontBox = QFontComboBox()
        layout.addWidget(self.fontBox)

        self.textEdit = QPlainTextEdit()
        layout.addWidget(self.textEdit)

        self.button2 = QPushButton("Отобразить текст")
        layout.addWidget(self.button2)

        return layout

    def _connect_signals(self):
        """Подключает кнопки панели управления к логике окна с часами."""

        self.button.clicked.connect(self.on_click1)
        self.button1.clicked.connect(self.on_click2)
        self.button2.clicked.connect(self.on_click3)
        self.textEdit.textChanged.connect(self.on_click3_change)
        self.fontBox.currentFontChanged.connect(self.onFontChanged)

    def on_click0(self):
        self.window.view.setHidden(True)

    def on_click1(self):
        if self.button.text() == "Отобразить часы":
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

            self.button.setText("Спрятать часы")
        else:
            self.window.view.setHidden(True)
            self.window.digit_container.setFixedHeight(600)
            self.window.minute_tens.set_size(250)
            self.window.minute_tens.set_animation_digit_space(
                new_digit_space=0.8, old_digit_space=0.8
            )
            self.window.minute_units.set_size(250)
            self.window.minute_units.set_animation_digit_space(
                new_digit_space=0.8, old_digit_space=0.8
            )
            self.window.second_tens.set_size(250)
            self.window.second_tens.set_animation_digit_space(
                new_digit_space=0.8, old_digit_space=0.8
            )
            self.window.second_units.set_size(250)
            self.window.second_units.set_animation_digit_space(
                new_digit_space=0.8, old_digit_space=0.8
            )

            self.button.setText("Отобразить часы")

    def on_click2(self):
        if self.button1.text() == "Включить обратный отсчет":
            self.window.startCountDown(
                self.timeEdit.time().hour() * 60 + self.timeEdit.time().minute(),
                self.timeEdit.time().second(),
            )
            self.button1.setText("Выключить обратный отсчет")
        else:
            self.window.stopCountDown()
            self.button1.setText("Включить обратный отсчет")

    def on_click3(self):
        if self.button2.text() == "Отобразить текст":
            self.window.drawText(self.textEdit.toPlainText())
            self.button2.setText("Скрыть екст")
        else:
            self.window.hideText()
            self.button2.setText("Отобразить текст")

    def on_click3_change(self):
        if self.button2.text() == "Скрыть текст":
            self.window.drawText(self.textEdit.toPlainText())

    def onFontChanged(self):
        custom_font = self.fontBox.currentFont()
        custom_font.setPixelSize(80)
        self.window.label2.setFont(custom_font)


class Window(QWidget):
    """Отдельное окно с часами для вывода на второй экран."""

    def __init__(self):
        super().__init__()

        # --- Базовая сцена и канва для стрелок и циферблата ---
        self.high = self.height() * 1.5
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self._configure_scene()
        self._configure_view()

        # --- Текст-заглушка для демонстрации верстки ---
        text = (
            "Проблему лени автор раскрывает на примере жизни одного из своих героев. "
            "Писатель обращает внимание читателя на давнюю неразрывную «связь» жизни героя с ленью. "
            "Автор отмечает, что лень властвует, господствует над героем, превращая его в своего пленника, заложника. "
            "Чехов подчеркивает, что его персонаж, с одной стороны, прекрасно понимает, что именно «моя она» – причина "
            "всех его несчастий; с другой стороны, указывает автор, его герой и не пытается хотя бы каким-то образом "
            "противостоять этому пороку."
        )

        # --- Основной вертикальный контейнер ---
        self.main_layout = QVBoxLayout()
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.view)

        # --- Составные блоки интерфейса ---
        self._build_label(text)
        self._build_digits()
        self._build_text_label()

        basedir = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.abspath(".")
        self._build_clock_face(basedir)
        self._build_hour_arrow(basedir)
        self._build_minute_arrow(basedir)
        self._build_second_arrow(basedir)

        self.setLayout(self.main_layout)

        # --- Инициализация времени и таймеров ---
        self._initialize_time_state()
        self._configure_timer()

    def _configure_scene(self):
        """Готовит сцену с чёрным фоном под циферблат."""
        self.scene.setBackgroundBrush(QBrush(Qt.black))
        self.scene.setSceneRect(0, 0, self.high, self.high)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.scene.setPalette(palette)
        self.setPalette(palette)

    def _configure_view(self):
        """Настраивает область отображения QGraphicsView."""
        self.view.setFixedHeight(self.high)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setStyleSheet("border: 0px")
        self.view.setRenderHint(QPainter.HighQualityAntialiasing)
        self.view.setScene(self.scene)

    def _build_label(self, text):
        """Выводит верхний текстовый блок-заглушку."""
        self.label = QLabel(
            f"Stack Overflow <h1 style=\"color: rgb(250, 250, 250);\">{text * 2}</h1>",
            alignment=Qt.AlignHCenter,
        )

    def _build_digits(self):
        """Создаёт четыре анимированные цифры и разделитель."""
        self.digit_container = QWidget()
        self.digit_container.setFixedHeight(400)

        digit_layout = QHBoxLayout(self.digit_container)
        digit_layout.setContentsMargins(0, 80, 0, 0)
        digit_layout.setSpacing(0)
        digit_layout.setAlignment(Qt.AlignCenter)

        basedir = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.abspath(".")

        self.minute_tens = AnimatedDigit(
            self, image_folder=os.path.join(basedir, "images_white"), new_digit_space=0.8
        )
        self.minute_units = AnimatedDigit(
            self, image_folder=os.path.join(basedir, "images_white"), size=170, new_digit_space=0.3
        )
        self.second_tens = AnimatedDigit(
            self, image_folder=os.path.join(basedir, "images_grey"), size=170, new_digit_space=0.3
        )
        self.second_units = AnimatedDigit(
            self, image_folder=os.path.join(basedir, "images_grey"), new_digit_space=0.8
        )

        digit_layout.addWidget(self.minute_tens)
        digit_layout.addWidget(self.minute_units)

        self.colon_label = QLabel(":")
        self.colon_label.setAlignment(Qt.AlignCenter)
        self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
        digit_layout.addWidget(self.colon_label)

        digit_layout.addWidget(self.second_tens)
        digit_layout.addWidget(self.second_units)

        self.main_layout.addWidget(self.digit_container, alignment=Qt.AlignCenter)

    def _build_text_label(self):
        """Плейсхолдер для текста проповеди/объявлений."""
        palette = self.palette()
        palette.setColor(QPalette.WindowText, Qt.white)

        self.label2 = QLabel("", alignment=Qt.AlignHCenter)
        self.label2.setPalette(palette)
        self.font = QFont("Arial", 80)
        self.label2.setFont(self.font)
        self.label2.setWordWrap(True)
        self.label2.setHidden(True)

        self.main_layout.addWidget(self.label2)

    def _build_clock_face(self, basedir):
        """Загружает SVG циферблата."""
        self.clock_face = QSvgWidget()
        self.clock_face.setFixedSize(self.high, self.high)
        self.clock_face.load(os.path.join(basedir, "деления_и_цифры.svg"))
        self.scene.addWidget(self.clock_face)

    def _build_hour_arrow(self, basedir):
        """Создаёт часовую стрелку и задаёт ось вращения."""
        renderer = QSvgRenderer(os.path.join(basedir, "hour_arrow.svg"))
        self.rb01 = QGraphicsSvgItem()
        self.rb01.setSharedRenderer(renderer)
        self.rb01.setScale(self.high / 543)

        transX0 = self.rb01.boundingRect().width() * 0.5
        transY0 = self.rb01.boundingRect().height() - self.rb01.boundingRect().width() * 0.5
        transX = self.high * (21 / 543)
        transY = self.high * (152 / 543)
        print(transX, transY)

        self.rb01.setTransformOriginPoint(transX0, transY0)
        deltaX = transX - transX0
        deltaY = transY - transY0
        self.rb01.setX(self.high * (0.5 - 21 / 543) + deltaX)
        self.rb01.setY(self.high * (0.5 - 152 / 543) + deltaY)
        self.rb01.setRotation(random.uniform(0, 360))

        self.scene.addItem(self.rb01)

    def _build_minute_arrow(self, basedir):
        """Создаёт минутную стрелку."""
        renderer = QSvgRenderer(os.path.join(basedir, "минутная_стрелка.svg"))
        self.rb02 = QGraphicsSvgItem()
        self.rb02.setSharedRenderer(renderer)
        self.rb02.setScale(self.high / 543)

        transX02 = self.rb02.boundingRect().width() * 0.5
        transY02 = self.rb02.boundingRect().height() - self.rb02.boundingRect().width() * 0.5
        transX2 = self.high * (21 / 543)
        transY2 = self.high * (245 / 543)
        print(transX2, transY2)

        self.rb02.setTransformOriginPoint(transX02, transY02)
        deltaX2 = transX2 - transX02
        deltaY2 = transY2 - transY02
        self.rb02.setX(self.high * (0.5 - 21 / 543) + deltaX2)
        self.rb02.setY(self.high * (0.5 - 245 / 543) + deltaY2)
        self.rb02.setRotation(random.uniform(0, 360) - 0.2)

        self.scene.addItem(self.rb02)

    def _build_second_arrow(self, basedir):
        """Создаёт секундную стрелку."""
        renderer = QSvgRenderer(os.path.join(basedir, "секундная_стрелка.svg"))
        self.rb03 = QGraphicsSvgItem()
        self.rb03.setSharedRenderer(renderer)
        self.rb03.setScale(0.25 * self.high / 543)

        transX03 = self.rb03.boundingRect().width() * 0.5
        transY03 = self.rb03.boundingRect().height() - self.rb03.boundingRect().width() * 4
        transX3 = self.high * (transX03 / 543)
        transY3 = self.high * (transY03 / 543)
        print(transX3, transY3)

        self.rb03.setTransformOriginPoint(transX03, transY03)
        deltaX3 = transX3 - transX03
        deltaY3 = transY3 - transY03
        self.rb03.setX(self.high * (0.5 - transX03 / 543) + deltaX3)
        self.rb03.setY(self.high * (0.5 - transY03 / 543) + deltaY3)
        self.rb03.setRotation(360 * 30 / 60)

        self.scene.addItem(self.rb03)

    def _initialize_time_state(self):
        """Сохраняет исходные значения времени и состояния обратного отсчёта."""
        self.second = int(time.strftime("%S"))
        self.start_minute = int(time.strftime("%M"))
        self.start_hour = int(time.strftime("%H"))

        self.countdown_minute = 1
        self.countdown_second = 0
        self.countdownEvent = False
        self.flickNum = 7

    def _configure_timer(self):
        """Таймер, который двигает стрелки и отсчитывает время."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate1deg)
        self.timer.start(1000)
        self.stopCountDown()

    def changeClockDivisions(self, high):
        self.clock_face.setFixedSize(high, high)

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
        self.second = self.second + 1
        self.rb03.setRotation(360 * (int(time.strftime("%S"))) / 60)
        self.rb02.setRotation(360 * (int(time.strftime("%M")) + int(time.strftime("%S")) / 60) / 60)
        self.rb01.setRotation(
            360 * (int(time.strftime("%H")) + int(time.strftime("%M")) / 60 + (int(time.strftime("%S")) / 60) / 60) / 12
        )
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

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.scene.setPalette(palette)
        self.setPalette(palette)
        self.changeClock(self.high)
        self.view.setFixedHeight(self.high)
        self.view.setAlignment(Qt.AlignHCenter)

    def countdown(self):
        if self.countdown_minute == 0 and self.countdown_second < 6:
            print("yep")
            self.flick()
        if self.countdown_second == 0:
            self.countdown_minute -= 1
            self.countdown_second = 59
        elif self.countdown_minute >= 0:
            self.countdown_second -= 1
        if self.countdown_minute >= 0:
            self.minute_tens.animate_digit_change(self.countdown_minute // 10)
            self.minute_units.animate_digit_change(self.countdown_minute % 10)
            self.second_tens.animate_digit_change(self.countdown_second // 10)
            self.second_units.animate_digit_change(self.countdown_second % 10)

    def flick(self):
        if self.flickNum % 2 == 1 and self.flickNum > 1:
            self.scene.setBackgroundBrush(QBrush(Qt.black))
            palette = self.palette()
            palette.setColor(self.backgroundRole(), Qt.black)
            self.scene.setPalette(palette)
            self.setPalette(palette)
            self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
            self.flickNum -= 1
        elif self.flickNum > 1:
            dark_red = QColor(139, 0, 0)

            self.scene.setBackgroundBrush(QBrush(dark_red))
            palette = self.palette()
            palette.setColor(self.backgroundRole(), dark_red)
            self.scene.setPalette(palette)
            self.setPalette(palette)
            self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: rgb(139, 0, 0);")
            self.flickNum -= 1
            print(self.flickNum)
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

    def addZeros(self, number):
        if number < 10:
            return "0" + str(number)
        return str(number)

    def doRotation(self):
        self.second = self.second + 1
        self.rb03.setRotation(360 * (self.second) / 60)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
