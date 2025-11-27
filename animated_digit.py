"""Вспомогательные виджеты для анимированных цифр обратного отсчёта."""

from PyQt5.QtCore import (
    QPoint,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QTimer,
    Qt,
    pyqtProperty,
)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect


class AnimatedDigit(QLabel):
    """Отображает одну цифру с анимацией смены и пульсации."""

    def __init__(self, parent=None, image_folder="images", size=200, new_digit_space=0.5, old_digit_space=0.5):
        super().__init__(parent)

        # --- Базовые настройки внешнего вида ---
        self.image_folder = image_folder
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.size = size
        self.new_digit_space = 1 / new_digit_space
        self.old_digit_space = 1 / old_digit_space
        self.setFixedSize(self.size, self.size)

        # --- Исходное состояние цифры ---
        self.current_digit = 0
        self.original_pixmap = QPixmap(f"{self.image_folder}/digit_{self.current_digit}.png")
        self.setPixmap(QPixmap(f"{self.image_folder}/digit_{self.current_digit}.png"))

        # --- Эффекты прозрачности и масштабирования ---
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1)
        self._scale_factor = 1.0
        self.is_animating = False

    # ------------------------------------------------------------------
    # Публичные методы для настройки
    # ------------------------------------------------------------------
    def set_digit(self, digit):
        self.current_digit = digit
        self.setPixmap(QPixmap(f"{self.image_folder}/digit_{self.current_digit}.png"))

    def set_animation_digit_space(self, new_digit_space=0.5, old_digit_space=0.5):
        self.new_digit_space = 1 / new_digit_space
        self.old_digit_space = 1 / old_digit_space

    def set_size(self, size):
        self.size = size
        self.setFixedSize(self.size, self.size)

    # ------------------------------------------------------------------
    # Анимация смены цифры
    # ------------------------------------------------------------------
    def animate_digit_change(self, new_digit):
        if self.current_digit == new_digit:
            return

        # --- Подготавливаем новый слой с цифрой ---
        self.new_digit_label = QLabel(self.parent())
        self.new_digit_label.setPixmap(QPixmap(f"{self.image_folder}/digit_{new_digit}.png"))
        self.new_digit_label.setAlignment(Qt.AlignCenter)
        self.new_digit_label.setScaledContents(True)
        self.new_digit_label.setFixedSize(self.size, self.size)
        self.new_digit_label.move(self.x(), -self.height() / self.new_digit_space)

        new_opacity_effect = QGraphicsOpacityEffect(self.new_digit_label)
        self.new_digit_label.setGraphicsEffect(new_opacity_effect)

        # --- Анимации появления новой цифры ---
        new_opacity_animation = QPropertyAnimation(new_opacity_effect, b"opacity")
        new_opacity_animation.setDuration(500)
        new_opacity_animation.setStartValue(0)
        if self.new_digit_space < 0.6:
            new_opacity_animation.setKeyValueAt(0.3, 0.6)
        new_opacity_animation.setEndValue(1)

        self.new_digit_label.show()

        self.new_digit_animation = QPropertyAnimation(self.new_digit_label, b"pos")
        self.new_digit_animation.setDuration(500)
        self.new_digit_animation.setStartValue(self.pos() - QPoint(0, self.height()) / self.new_digit_space)
        self.new_digit_animation.setEndValue(self.pos())

        # --- Анимации ухода старой цифры ---
        self.old_digit_animation = QPropertyAnimation(self, b"pos")
        self.old_digit_animation.setDuration(500)
        self.old_digit_animation.setStartValue(self.pos())
        self.old_digit_animation.setEndValue(self.pos() + QPoint(0, self.height()) / self.old_digit_space)

        old_opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        old_opacity_animation.setDuration(500)
        old_opacity_animation.setStartValue(1)
        old_opacity_animation.setEndValue(0)

        # --- Группируем анимации и запускаем ---
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

    # ------------------------------------------------------------------
    # Анимация пульсации (используется при завершении таймера)
    # ------------------------------------------------------------------
    def setup_animations(self):
        # --- Начальное увеличение ---
        self.initial_scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.initial_scale_animation.setDuration(500)
        self.initial_scale_animation.setStartValue(1.0)
        self.initial_scale_animation.setEndValue(1.1)

        # --- Пульсация вперёд/назад ---
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

        # --- Группы анимаций ---
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
        if hasattr(self, "full_animation_group"):
            self.full_animation_group.stop()
        self.is_animating = False
        self.scale_factor = 1.0
        self.update()
        self.opacity_effect.setOpacity(1)

    # ------------------------------------------------------------------
    # Свойство масштабирования для анимаций
    # ------------------------------------------------------------------
    @pyqtProperty(float)
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, factor):
        self._scale_factor = factor
        self.update()

    # ------------------------------------------------------------------
    # Отрисовка учитывая текущий масштаб
    # ------------------------------------------------------------------
    def paintEvent(self, event):  # noqa: N802 - PyQt signature
        if self.is_animating:
            painter = QPainter(self)
            scaled_pixmap = self.original_pixmap.scaled(
                self.size * self._scale_factor,
                self.size * self._scale_factor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            x = (self.width() - scaled_pixmap.width()) / 2
            y = (self.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            super().paintEvent(event)


__all__ = ["AnimatedDigit"]
