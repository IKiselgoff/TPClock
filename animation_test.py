import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsOpacityEffect, QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, Qt, QTimer, QPoint, QSequentialAnimationGroup, \
    pyqtProperty
from PyQt5.QtGui import QPixmap, QPalette, QColor, QTransform, QPainter


class AnimatedDigit(QLabel):
    def __init__(self, parent=None, image_folder="images", size = 200, new_digit_space = 0.5, old_digit_space = 0.5):
        super().__init__(parent)
        self.image_folder = image_folder
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.size = size
        self.new_digit_space = 1/new_digit_space
        self.old_digit_space = 1/old_digit_space
        self.setFixedSize(self.size, self.size)  # Adjust size as needed
        self.current_digit = 0
        self.original_pixmap = QPixmap(f'{self.image_folder}/digit_{self.current_digit}.png')
        self.setPixmap(QPixmap(f'{self.image_folder}/digit_{self.current_digit}.png'))
        #self.setStyleSheet("background-color: black;")  # Set background color to black

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1)
        # Инициализация _scale_factor
        self._scale_factor = 1.0
        self.is_animating = False  # Флаг для контроля анимации

    def set_digit(self, digit):
        self.current_digit = digit
        self.setPixmap(QPixmap(f'{self.image_folder}/digit_{self.current_digit}.png'))

    def set_animation_digit_space(self, new_digit_space =0.5 , old_digit_space=0.5 ):
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
        self.new_digit_label.move(self.x(), - self.height()/self.new_digit_space)
        #self.new_digit_label.setStyleSheet("background-color: black;")  # Set background color to black

        new_opacity_effect = QGraphicsOpacityEffect(self.new_digit_label)
        self.new_digit_label.setGraphicsEffect(new_opacity_effect)
        new_opacity_animation = QPropertyAnimation(new_opacity_effect, b"opacity")
        new_opacity_animation.setDuration(500)
        new_opacity_animation.setStartValue(0)
        if (self.new_digit_space < 0.6):
            new_opacity_animation.setKeyValueAt(0.3, 0.6)

        new_opacity_animation.setEndValue(1)

        self.new_digit_label.show()

        self.new_digit_animation = QPropertyAnimation(self.new_digit_label, b"pos")
        self.new_digit_animation.setDuration(500)
        self.new_digit_animation.setStartValue(self.pos() - QPoint(0, self.height())/self.new_digit_space)
        self.new_digit_animation.setEndValue(self.pos())

        self.old_digit_animation = QPropertyAnimation(self, b"pos")
        self.old_digit_animation.setDuration(500)
        self.old_digit_animation.setStartValue(self.pos())
        self.old_digit_animation.setEndValue(self.pos() + QPoint(0, self.height())/self.old_digit_space)
        old_opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        old_opacity_animation.setDuration(500)
        old_opacity_animation.setStartValue(1)
        #old_opacity_animation.setKeyValueAt(0.7, 0.4)
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
        self.move(self.x(), self.y() - self.height()/self.old_digit_space)
        self.opacity_effect.setOpacity(1)  # Reset opacity for the next animation

    def setup_animations(self):
        # Начальная анимация изменения масштаба до 1.2
        self.initial_scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.initial_scale_animation.setDuration(500)
        self.initial_scale_animation.setStartValue(1.0)
        self.initial_scale_animation.setEndValue(1.1)

        # Анимация изменения масштаба
        self.scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation.setDuration(1000)  # Половина периода
        self.scale_animation.setStartValue(1.1)
        self.scale_animation.setEndValue(0.9)

        self.scale_animation_reverse = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation_reverse.setDuration(1000)  # Половина периода
        self.scale_animation_reverse.setStartValue(0.9)
        self.scale_animation_reverse.setEndValue(1.1)

        # Создаем анимацию для изменения прозрачности
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(1000)  # Половина периода
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.5)

        self.opacity_animation_reverse = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation_reverse.setDuration(1000)  # Половина периода
        self.opacity_animation_reverse.setStartValue(0.5)
        self.opacity_animation_reverse.setEndValue(1.0)

        # Группируем анимации в параллельную группу
        self.pulsing_animation_group = QParallelAnimationGroup()
        self.pulsing_animation_group.addAnimation(self.scale_animation)
        self.pulsing_animation_group.addAnimation(self.opacity_animation)

        self.reverse_animation_group = QParallelAnimationGroup()
        self.reverse_animation_group.addAnimation(self.scale_animation_reverse)
        self.reverse_animation_group.addAnimation(self.opacity_animation_reverse)

        # Создаем последовательную группу для циклического воспроизведения
        self.full_animation_group = QSequentialAnimationGroup()
        self.full_animation_group.addAnimation(self.pulsing_animation_group)
        self.full_animation_group.addAnimation(self.reverse_animation_group)


    def animate_pulsing(self, t_start):
        self.is_animating = True
        self.setup_animations()

        # Сначала выполняем начальную анимацию
        QTimer.singleShot(t_start, self.initial_scale_animation.start)

        # После завершения начальной анимации запускаем зацикленную анимацию
        self.initial_scale_animation.finished.connect(self.start_looping_animation)

    def start_looping_animation(self):
        self.full_animation_group.setLoopCount(-1)  # Зацикливаем параллельную часть
        self.full_animation_group.start()


    def stop_animation(self):
        # Используем QTimer для задержки начала анимации
        #QTimer.singleShot(t_start, self.full_animation_group.start)
        # Останавливаем анимацию
        if hasattr(self, 'full_animation_group'):
            self.full_animation_group.stop()
        self.is_animating = False
        # Сбрасываем масштаб и прозрачность к исходным значениям
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
        if self.is_animating == True:
            # Переопределяем paintEvent для отрисовки с изменением масштаба
            painter = QPainter(self)
            scaled_pixmap = self.original_pixmap.scaled(self.size * self._scale_factor, self.size * self._scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled_pixmap.width()) / 2
            y = (self.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            # Вызываем стандартное поведение QLabel
            super().paintEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Countdown Timer")
        self.setGeometry(100, 100, 500, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.minute_tens = AnimatedDigit(self, image_folder="images_white")
        self.minute_units = AnimatedDigit(self, image_folder="images_white")
        self.second_tens = AnimatedDigit(self, image_folder="images_grey")
        self.second_units = AnimatedDigit(self, image_folder="images_grey",old_digit_space=0.5,new_digit_space=0.5)

        self.layout.addWidget(self.minute_tens)
        self.layout.addWidget(self.minute_units)
        self.colon_label = QLabel(":")
        self.colon_label.setAlignment(Qt.AlignCenter)
        #self.colon_label.setStyleSheet("color: white; font-size: 100px; background-color: black;")
        self.layout.addWidget(self.colon_label)
        self.layout.addWidget(self.second_tens)
        self.layout.addWidget(self.second_units)

        # Запускаем анимацию пульсации
        self.minute_tens.animate_pulsing(2000)
        #QTimer.singleShot(5000, self.minute_tens.stop_animation)

        self.minutes = 1
        self.seconds = 10

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        # Set the background color of the main window to black
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(Qt.black))
        self.setPalette(palette)

        self.update_display()

    def update_display(self):
        self.minute_tens.set_digit(self.minutes // 10)
        self.minute_units.set_digit(self.minutes % 10)
        self.second_tens.set_digit(self.seconds // 10)
        self.second_units.set_digit(self.seconds % 10)

    def update_time(self):
        if self.seconds == 0:
            if self.minutes == 0:
                self.timer.stop()
                return
            self.minutes -= 1
            self.seconds = 59
        else:
            self.seconds -= 1

        self.animate_digits()

    def animate_digits(self):
        self.minute_tens.animate_digit_change(self.minutes // 10)
        self.minute_units.animate_digit_change(self.minutes % 10)
        self.second_tens.animate_digit_change(self.seconds // 10)
        self.second_units.animate_digit_change(self.seconds % 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
