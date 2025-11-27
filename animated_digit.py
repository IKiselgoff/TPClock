# animated_digit.py
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QPropertyAnimation, QRect

class AnimatedDigit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.current_digit = QLabel("0", self)
        self.next_digit = QLabel("0", self)
        self.layout.addWidget(self.current_digit)
        self.layout.addWidget(self.next_digit)
        self.next_digit.hide()
        self.animation = QPropertyAnimation(self.current_digit, b"geometry")
        self.animation.setDuration(500)
        self.animation.finished.connect(self.on_animation_finished)

    def set_digit(self, digit):
        self.next_digit.setText(str(digit))
        self.next_digit.show()
        self.animation.setStartValue(QRect(0, 0, self.width(), self.height()))
        self.animation.setEndValue(QRect(0, -self.height(), self.width(), self.height()))
        self.animation.start()

    def on_animation_finished(self):
        self.current_digit.setText(self.next_digit.text())
        self.current_digit.setGeometry(0, 0, self.width(), self.height())
        self.next_digit.hide()
