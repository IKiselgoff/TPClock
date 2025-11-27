import os
import random
import sys
# from random import random
import time
#from animated_digit import AnimatedDigit

from animation_test import AnimatedDigit
from PyQt5.QtCore import QTimer

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QTime,  pyqtSignal, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QBrush, QPalette, QFontMetrics, QFont, QColor
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
    QSizePolicy,
    QWidget,
    QPlainTextEdit, QHBoxLayout
)
from PyQt5.QtWidgets import QGraphicsScene, \
    QGraphicsView, QPlainTextEdit


# Подкласс QMainWindow для настройки основного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clock Control Panel")
        self.window = Window()
        self.window.setMinimumSize(543, 543)
        self.window.show()


        layout = QVBoxLayout()
        widgets = [
            QPushButton,
            #QCheckBox,
            #QComboBox,
            #QDateEdit,
            #QDateTimeEdit,
            #QDial,
            #QDoubleSpinBox,
            QFontComboBox,
            #QLCDNumber,
            #QLabel,
            QPlainTextEdit,
            #QProgressBar,
            #QSlider,
            #QSpinBox,
            QTimeEdit,
        ]



        self.button = QPushButton('Спрятать часы')
        layout.addWidget(self.button)

        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        self.timeEdit.setTime(QTime(0,5, 0))
        layout.addWidget(self.timeEdit)

        self.button1 = QPushButton('Включить обратный отсчет')
        layout.addWidget(self.button1)

        self.fontBox = QFontComboBox()
        layout.addWidget(self.fontBox)

        self.textEdit = QPlainTextEdit()
        layout.addWidget(self.textEdit)

        self.button2 = QPushButton('Отобразить текст')
        layout.addWidget(self.button2)





        '''for w in widgets:
            if w==QPushButton:
                self.button = w('Отобразить часы')
                layout.addWidget(self.button)
            else:
                layout.addWidget(w())'''

        widget = QWidget()
        widget.setLayout(layout)

        self.button.clicked.connect(self.on_click1)
        self.button1.clicked.connect(self.on_click2)
        self.button2.clicked.connect(self.on_click3)
        self.textEdit.textChanged.connect(self.on_click3_change)
        self.fontBox.currentFontChanged.connect(self.onFontChanged)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(widget)

    def on_click0(self):
        self.window.view.setHidden(True)

    def on_click1(self):
        if self.button.text()=='Отобразить часы':
            self.window.view.setHidden(False)
            self.window.digit_container.setFixedHeight(400)  # Установите нужную высоту в пикселях
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
            self.window.digit_container.setFixedHeight(600)  # Установите нужную высоту в пикселях
            self.window.minute_tens.set_size(250)
            self.window.minute_tens.set_animation_digit_space(new_digit_space=0.8,old_digit_space=0.8)
            self.window.minute_units.set_size(250)
            self.window.minute_units.set_animation_digit_space(new_digit_space=0.8,old_digit_space=0.8)
            self.window.second_tens.set_size(250)
            self.window.second_tens.set_animation_digit_space(new_digit_space=0.8,old_digit_space=0.8)
            self.window.second_units.set_size(250)
            self.window.second_units.set_animation_digit_space(new_digit_space=0.8,old_digit_space=0.8)

            self.button.setText('Отобразить часы')

    def on_click2(self):
        if self.button1.text()=='Включить обратный отсчет':
            self.window.startCountDown(self.timeEdit.time().hour()*60 +self.timeEdit.time().minute(),self.timeEdit.time().second())
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






class Window(QWidget):
    def __init__(self):
        super().__init__()




        '''self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setFixedSize(self.height(), self.height())
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        #self.setCentralWidget(self.widgetSvg)
        self.widgetSvg.load("/Users/admin/Downloads/деления_и_цифры.svg")'''

        self.high = self.height()*1.5



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


        #self.label = QLabel('Stack Overflow <h1 style="color: rgb(250, 55, 55);">QLabel</h1>',alignment=Qt.AlignHCenter, parent=self.view)
        #self.view_layout = QVBoxLayout()

        #self.view_layout.addWidget(self.label)
        #self.view.setLayout(self.view_layout)




        #scene_layout = QGraphicsLinearLayout(Qt.Horizontal)


        #form = QGraphicsWidget()

        #form.setPalette(p)
        #form.setLayout(scene_layout)

        #self.scene.addItem(form)
        text = 'Проблему лени автор раскрывает на примере жизни одного из своих героев. Писатель обращает внимание читателя на давнюю неразрывную «связь» жизни героя с ленью. Автор отмечает, что лень властвует, господствует над героем, превращая его в своего пленника, заложника. Чехов подчеркивает, что его персонаж, с одной стороны, прекрасно понимает, что именно «моя она» – причина всех его несчастий; с другой стороны, указывает автор, его герой и не пытается хотя бы каким-то образом противостоять этому пороку.'

        self.main_layout = QVBoxLayout()
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.view)
        self.label = QLabel('Stack Overflow <h1 style="color: rgb(250, 250, 250);">'+text*2+'</h1>',
                            alignment=Qt.AlignHCenter) #rgb(250, 55, 55)
        # self.label1 = QLabel('',alignment=Qt.AlignCenter)
        # p.setColor(QPalette.WindowText, Qt.white)
        # self.label1.setPalette(p)
        # self.label1.setFont(QFont('Arial', 200))
        # self.label1.setHidden(True)
        # self.main_layout.addWidget(self.label1)

        # Create a container widget for the animated digits
        self.digit_container = QWidget()

        self.digit_container.setFixedHeight(400)  # Установите нужную высоту в пикселях
        self.digit_layout = QHBoxLayout(self.digit_container)
        self.digit_layout.setContentsMargins(0, 80, 0, 0)
        self.digit_layout.setSpacing(0)
        self.digit_layout.setAlignment(Qt.AlignCenter)  # Выровнять содержимое по центру

        # Определяем путь к ресурсам
        if hasattr(sys, '_MEIPASS'):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.abspath(".")

        # Initialize the animated digits
        self.minute_tens = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_white"), new_digit_space=0.8)
        self.minute_units = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_white"),size=170, new_digit_space=0.3)
        self.second_tens = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_grey"),size=170, new_digit_space=0.3)
        #self.second_tens.set_size(100)
        self.second_units = AnimatedDigit(self, image_folder=os.path.join(basedir, "images_grey"), new_digit_space=0.8)

        # Add the animated digits to the digit layout
        self.digit_layout.addWidget(self.minute_tens)
        self.digit_layout.addWidget(self.minute_units)
        self.colon_label = QLabel(":")
        self.colon_label.setAlignment(Qt.AlignCenter)
        self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
        self.digit_layout.addWidget(self.colon_label)
        self.digit_layout.addWidget(self.second_tens)
        self.digit_layout.addWidget(self.second_units)

        # Add the digit container to the main layout
        self.main_layout.addWidget(self.digit_container, alignment=Qt.AlignCenter)

        self.label2 = QLabel('', alignment=Qt.AlignHCenter)
        p.setColor(QPalette.WindowText, Qt.white)
        self.label2.setPalette(p)
        self.font = QFont('Arial', 80)
        self.label2.setFont(self.font)
        #self.label2.setFixedHeight(200)
        #self.label2.setFixedWidth(self.high)
        self.label2.setWordWrap(True)
        self.label2.setHidden(True)
        self.main_layout.addWidget(self.label2)
        self.setLayout(self.main_layout)

        '''self.label = QLabel('Stack Overflow <h1 style="color: rgb(250, 55, 55);">QLabel,</h1>', alignment=Qt.AlignCenter)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.label)
        proxy.setX(-100)
        proxy.setY(-100)
        self.scene.addItem(proxy)'''
        #self.label.set



        self.rb0 = QSvgWidget()
        self.rb0.setFixedSize(self.high, self.high)
        self.rb0.load(os.path.join(basedir, 'деления_и_цифры.svg'))
        proxy_rb0 = self.scene.addWidget(self.rb0)
        #proxy_rb0.setRotation(0)
        #scene_layout.addItem(proxy_rb0)




        '''self.rb1 = QSvgWidget()
        self.rb1.setFixedSize(42, 173)
        self.rb1.load("/Users/admin/Downloads/hour_arrow.svg")
        proxy_rb1 = self.scene.addWidget(self.rb1)
        proxy_rb1.setRotation(75)
        scene_layout.addItem(proxy_rb1)'''

        renderer = QSvgRenderer(os.path.join(basedir, "hour_arrow.svg"))
        self.rb01 = QGraphicsSvgItem()

        self.rb01.setSharedRenderer(renderer)
        self.rb01.setScale(self.high/543)

        #self.rb01.setFixedSize(self.height()*42/543,self.height()*173/543)

        #self.rb01.moveBy(self.height()*(0.5-21/543),self.height()*(0.5-173/543))
        #self.rb01.setTransformOriginPoint(self.height()*(21/543),self.height()*(173/543))
        transX0 = self.rb01.boundingRect().width()*0.5
        transY0 = self.rb01.boundingRect().height()-self.rb01.boundingRect().width()*0.5
        transX = self.high*(21/543)
        transY = self.high*(152/543)
        print(transX,transY)
        self.rb01.setTransformOriginPoint(transX0,transY0)
        deltaX = transX-transX0 #-1/7.6114725833
        deltaY = transY-transY0 #-1/7.569838923
        self.rb01.setX(self.high*(0.5-21/543)+deltaX)
        self.rb01.setY(self.high*(0.5-152/543)+deltaY)
        #print(self.height(),koefX,koefX*180*transX)
        self.rb01.setRotation(random.uniform(0, 360))
        proxy_rb01 = self.scene.addItem(self.rb01)

        renderer2 = QSvgRenderer(os.path.join(basedir, "минутная_стрелка.svg"))
        self.rb02 = QGraphicsSvgItem()

        self.rb02.setSharedRenderer(renderer2)
        self.rb02.setScale(self.high / 543)

        transX02 = self.rb02.boundingRect().width() * 0.5
        transY02 = self.rb02.boundingRect().height() - self.rb02.boundingRect().width() * 0.5
        transX2 = self.high * (21 / 543)
        transY2 = self.high * (245 / 543)
        print(transX2, transY2)
        self.rb02.setTransformOriginPoint(transX02, transY02)
        deltaX2 = transX2 - transX02  # -1/7.6114725833
        deltaY2 = transY2 - transY02  # -1/7.569838923
        self.rb02.setX(self.high * (0.5 - 21 / 543) + deltaX2)
        self.rb02.setY(self.high * (0.5 - 245 / 543) + deltaY2)
        #self.rb02.moveBy(self.height() * (0.5 - 21 / 543), self.height() * (0.5 - 266/ 543))
        #self.rb02.setTransformOriginPoint(self.height() * (21 / 543), self.height() * (266 / 543))
        self.rb02.setRotation(random.uniform(0, 360)-0.2)
        proxy_rb02 = self.scene.addItem(self.rb02)
        #proxy_rb01.setRotation(75)
        #scene_layout.addItem(proxy_rb01)

        renderer3 = QSvgRenderer(os.path.join(basedir, "секундная_стрелка.svg"))
        self.rb03 = QGraphicsSvgItem()

        self.rb03.setSharedRenderer(renderer3)
        self.rb03.setScale(0.25*self.high / 543)

        transX03 = self.rb03.boundingRect().width() * 0.5
        transY03 = self.rb03.boundingRect().height() - self.rb03.boundingRect().width() * 4
        transX3 = self.high * (transX03 / 543)
        transY3 = self.high * (transY03 / 543)
        print(transX3, transY3)
        self.rb03.setTransformOriginPoint(transX03, transY03)
        deltaX3 = transX3 - transX03  # -1/7.6114725833
        deltaY3 = transY3 - transY03  # -1/7.569838923
        self.rb03.setX(self.high * (0.5 - transX03/ 543) + deltaX3)
        self.rb03.setY(self.high * (0.5 - transY03 / 543) + deltaY3)
        # self.rb02.moveBy(self.height() * (0.5 - 21 / 543), self.height() * (0.5 - 266/ 543))
        # self.rb02.setTransformOriginPoint(self.height() * (21 / 543), self.height() * (266 / 543))

        self.rb03.setRotation(360*30/60)
        proxy_rb02 = self.scene.addItem(self.rb03)

        self.second = int(time.strftime('%S'))
        self.start_minute = int(time.strftime('%M'))
        self.start_hour = int(time.strftime('%H'))

        self.countdown_minute = 1
        self.countdown_second = 0
        self.countdownEvent = False
        self.flickNum = 7
        #self.rotate1deg()

        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate1deg)
        self.timer.start(1000)
        self.stopCountDown()
        #self.timer = threading.Timer(1, self.rotate1deg)
        #self.timer.start()

    def changeClockDivisions(self,high):
        self.rb0.setFixedSize(high, high)

    def changeHourArrow(self,high):
        self.rb01.setScale(high / 543)
        transX0 = self.rb01.boundingRect().width() * 0.5
        transY0 = self.rb01.boundingRect().height() - self.rb01.boundingRect().width() * 0.5
        transX = high * (21 / 543)
        transY = high * (152 / 543)
        self.rb01.setTransformOriginPoint(transX0, transY0)
        deltaX = transX - transX0  # -1/7.6114725833
        deltaY = transY - transY0  # -1/7.569838923
        self.rb01.setX(high * (0.5 - 21 / 543) + deltaX)
        self.rb01.setY(high * (0.5 - 152 / 543) + deltaY)

    def changeMinuteArrow(self,high):
        self.rb02.setScale(high / 543)
        transX02 = self.rb02.boundingRect().width() * 0.5
        transY02 = self.rb02.boundingRect().height() - self.rb02.boundingRect().width() * 0.5
        transX2 = high * (21 / 543)
        transY2 = high * (245 / 543)
        self.rb02.setTransformOriginPoint(transX02, transY02)
        deltaX2 = transX2 - transX02  # -1/7.6114725833
        deltaY2 = transY2 - transY02  # -1/7.569838923
        self.rb02.setX(high * (0.5 - 21 / 543) + deltaX2)
        self.rb02.setY(high * (0.5 - 245 / 543) + deltaY2)

    def changeSecondArrow(self,high):
        self.rb03.setScale(0.25 * high / 543)
        transX03 = self.rb03.boundingRect().width() * 0.5
        transY03 = self.rb03.boundingRect().height() - self.rb03.boundingRect().width() * 4
        transX3 = high * (transX03 / 543)
        transY3 = high * (transY03 / 543)
        self.rb03.setTransformOriginPoint(transX03, transY03)
        deltaX3 = transX3 - transX03  # -1/7.6114725833
        deltaY3 = transY3 - transY03  # -1/7.569838923
        self.rb03.setX(high * (0.5 - transX03 / 543) + deltaX3)
        self.rb03.setY(high * (0.5 - transY03 / 543) + deltaY3)

    def changeClock(self,high):
        self.scene.setSceneRect(0, 0, high, high)
        self.changeClockDivisions(high)
        self.changeHourArrow(high)
        self.changeMinuteArrow(high)
        self.changeSecondArrow(high)



    def rotate1deg(self):
        self.second = self.second + 1
        #self.rb03.setRotation(360 * (self.second) / 60)
        #self.rb02.setRotation(360 * (self.start_minute+self.second/60) / 60)
        #self.rb01.setRotation(360 * (self.start_hour+self.start_minute/60+(self.second/60) / 60) / 12)
        self.rb03.setRotation(360 * (int(time.strftime('%S'))) / 60)
        self.rb02.setRotation(360 * (int(time.strftime('%M')) + int(time.strftime('%S')) / 60) / 60)
        self.rb01.setRotation(360 * (int(time.strftime('%H')) + int(time.strftime('%M')) / 60 + (int(time.strftime('%S')) / 60) / 60) / 12)
        self.scene.update()
        if self.countdownEvent:
            self.countdown()

    def startCountDown(self,minutes,seconds):
        self.countdown_minute = minutes
        self.countdown_second = seconds
        self.countdownEvent = True
        self.flickNum = 7
        self.view.setFixedHeight(self.high / 1.3)
        self.changeClock(self.high / 1.4)
        self.digit_container.setVisible(True)
        self.timer.start(1000)  # Start the timer to update every second

    def stopCountDown(self):
        self.countdownEvent = False
        #self.label1.setHidden(True)
        self.digit_container.setVisible(False)
        self.minute_tens.stop_animation()
        self.minute_units.stop_animation()
        self.second_tens.stop_animation()
        self.second_units.stop_animation()
        #self.timer.stop()  # Stop the timer
        self.scene.setBackgroundBrush(QBrush(Qt.black))
        #self.digit_container.setStyleSheet(
        #    "background-color: black;")
        self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.scene.setPalette(p)
        self.setPalette(p)
        self.changeClock(self.high)
        self.view.setFixedHeight(self.high)
        self.view.setAlignment(Qt.AlignHCenter)

    def countdown(self):
        if self.countdown_minute == 0 and self.countdown_second < 6:
            print('yep')
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
        if self.flickNum % 2 ==1 and self.flickNum>1:
            self.scene.setBackgroundBrush(QBrush(Qt.black))
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.black)
            self.scene.setPalette(p)
            self.setPalette(p)
            #self.digit_container.setStyleSheet(
            #    "background-color: black;")  # Set countdown container background to black
            self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: black;")
            self.flickNum-=1
        elif self.flickNum>1:
            # Define the dark red color using RGB values
            dark_red = QColor(139, 0, 0)

            self.scene.setBackgroundBrush(QBrush(dark_red))
            p = self.palette()
            p.setColor(self.backgroundRole(), dark_red)
            self.scene.setPalette(p)
            self.setPalette(p)
            #self.digit_container.setStyleSheet(
            #    "background-color: rgb(139, 0, 0);")  # Set countdown container background to dark red
            self.colon_label.setStyleSheet("color: white; font-size: 200px; background-color: rgb(139, 0, 0);")
            self.flickNum -= 1
            print(self.flickNum)
            if self.flickNum == 1:
                # Запускаем анимацию пульсации
                self.minute_tens.animate_pulsing(1000)
                self.minute_units.animate_pulsing(1500)
                self.second_tens.animate_pulsing(2000)
                self.second_units.animate_pulsing(2500)
                # QTimer.singleShot(5000, self.minute_tens.stop_animation)



    def drawText(self,text):
        self.view.setHidden(True)
        self.label2.setText(text)
        self.label2.setHidden(False)
    def hideText(self):
        self.view.setHidden(False)
        self.label2.setHidden(True)



    def addZeros(self,number):
        if number < 10:
            return '0' + str(number)
        else:
            return str(number)

    def doRotation(self):
        self.second = self.second + 1
        self.rb03.setRotation(360 * (self.second) / 60)










if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    #window = MainWindow()
    #window.show()

    sys.exit(app.exec_())
