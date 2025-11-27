"""Демонстрация работы AnimatedDigit в изолированном окне."""

import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QMainWindow, QWidget

from animated_digit import AnimatedDigit


class DemoWindow(QMainWindow):
    """Отдельное окно для ручного тестирования анимации цифр."""

    def __init__(self):
        super().__init__()

        # --- Базовая настройка окна ---
        self.setWindowTitle("Countdown Timer")
        self.setGeometry(100, 100, 500, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # --- Размещение четырёх цифр таймера ---
        self.layout = QHBoxLayout(self.central_widget)
        self.minute_tens = AnimatedDigit(self, image_folder="images_white")
        self.minute_units = AnimatedDigit(self, image_folder="images_white")
        self.second_tens = AnimatedDigit(self, image_folder="images_grey")
        self.second_units = AnimatedDigit(self, image_folder="images_grey", old_digit_space=0.5, new_digit_space=0.5)

        self.layout.addWidget(self.minute_tens)
        self.layout.addWidget(self.minute_units)
        self.colon_label = QLabel(":")
        self.colon_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.colon_label)
        self.layout.addWidget(self.second_tens)
        self.layout.addWidget(self.second_units)

        # --- Активация пульсации и стартовых значений ---
        self.minute_tens.animate_pulsing(2000)
        self.minutes = 1
        self.seconds = 10

        # --- Таймер тестового обратного отсчёта ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # --- Чёрный фон, как в основном окне ---
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
    window = DemoWindow()
    window.show()
    sys.exit(app.exec_())
