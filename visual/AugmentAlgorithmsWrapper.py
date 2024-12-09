from PyQt5.QtCore import QLine, QObject
from PyQt5.QtWidgets import QWidget, QRadioButton, QLineEdit, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, \
    QButtonGroup, QFileDialog, QComboBox

from augmenter.MoveAugmentor import MoveAugmentor, Direction, FillingRule


class LabeledSomething(QWidget):
    def __init__(self, other: QObject):
        super().__init__()
        self.label = QLabel("[no label]")
        self.instance = other

        base_layout = QHBoxLayout()
        self.setLayout(base_layout)

        base_layout.addWidget(self.label)
        base_layout.addWidget(self.instance)

        self.hide()


class AugmentAlgorithmsWrapper(QWidget):
    def __init__(self):
        super().__init__()
        self.statistic_color_correction_reference_pic = None

        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        self.button_group = QButtonGroup(self)

        self.add_noise_radiobutton = QRadioButton("Добавить случайный шум")
        self.blur_mean_radiobutton = QRadioButton("Размытие по среднему")
        self.blur_gauss_radiobutton = QRadioButton("Размытие по Гауссу")
        self.equalize_radiobutton = QRadioButton("Эквализация")
        self.statistic_color_correction_radiobutton = QRadioButton("Статистическая цветокоррекция")
        self.move_radiobutton = QRadioButton("Сдвиг")
        self.motion_blur_radiobutton = QRadioButton("Motion Blur")

        self.button_group.addButton(self.add_noise_radiobutton)
        self.button_group.addButton(self.blur_mean_radiobutton)
        self.button_group.addButton(self.blur_gauss_radiobutton)
        self.button_group.addButton(self.equalize_radiobutton)
        self.button_group.addButton(self.statistic_color_correction_radiobutton)
        self.button_group.addButton(self.move_radiobutton)
        self.button_group.addButton(self.motion_blur_radiobutton)

        self.add_noise_radiobutton.toggled.connect(self._on_add_noise_radiobutton_toggle)
        self.blur_mean_radiobutton.toggled.connect(self._on_blur_mean_radiobutton_toggle)
        self.blur_gauss_radiobutton.toggled.connect(self._on_blur_gauss_radiobutton_toggle)
        self.equalize_radiobutton.toggled.connect(self._on_equalize_radiobutton_toggle)
        self.statistic_color_correction_radiobutton.toggled.connect(self._on_statistic_color_correction_radiobutton_toggle)
        self.move_radiobutton.toggled.connect(self._on_move_radiobutton_toggle)
        self.motion_blur_radiobutton.toggled.connect(self._on_motion_blur_radiobutton_toggle)


        delimiter = QPushButton("")
        delimiter.setDisabled(True)
        delimiter.setFixedHeight(3)
        delimiter.setStyleSheet("background-color: #239923; border: none")
        self.base_layout.addWidget(delimiter)


        self.base_layout.addWidget(self.add_noise_radiobutton)
        self.base_layout.addWidget(self.blur_mean_radiobutton)
        self.base_layout.addWidget(self.blur_gauss_radiobutton)
        self.base_layout.addWidget(self.equalize_radiobutton)
        self.base_layout.addWidget(self.statistic_color_correction_radiobutton)
        self.base_layout.addWidget(self.move_radiobutton)
        self.base_layout.addWidget(self.motion_blur_radiobutton)

        delimiter = QPushButton("")
        delimiter.setDisabled(True)
        delimiter.setFixedHeight(3)
        delimiter.setStyleSheet("background-color: #239923; border: none")
        self.base_layout.addWidget(delimiter)
        self.base_layout.addStretch(1)

        self.box = QWidget()
        self.box.setFixedHeight(400)
        self.box_layout = QVBoxLayout()
        self.box.setLayout(self.box_layout)

        self.lineedit = LabeledSomething(QLineEdit())
        self.button = LabeledSomething(QPushButton())
        self.combo_1 = LabeledSomething(QComboBox())
        self.combo_2 = LabeledSomething(QComboBox())

        self.box_layout.addStretch(1)
        self.box_layout.addWidget(self.lineedit)
        self.box_layout.addWidget(self.button)
        self.box_layout.addWidget(self.combo_1)
        self.box_layout.addWidget(self.combo_2)
        self.box_layout.addStretch(1)

        self.base_layout.addWidget(self.box)

        self.base_layout.addStretch(1)


    def _on_add_noise_radiobutton_toggle(self, checked: bool):
        if checked:
            self.lineedit.show()
            self.lineedit.label.setText("Дисперсия:")
        else: self.lineedit.hide()

    def _on_blur_mean_radiobutton_toggle(self, checked: bool):
        if checked:
            self.lineedit.show()
            self.lineedit.label.setText("Размер полуядра усреднения:")
        else: self.lineedit.hide()

    def _on_blur_gauss_radiobutton_toggle(self, checked: bool):
        if checked:
            self.lineedit.show()
            self.lineedit.label.setText("Дисперсия:")
        else: self.lineedit.hide()

    def _on_equalize_radiobutton_toggle(self, checked: bool):
        return

    def _on_move_radiobutton_toggle(self, checked: bool):
        if checked:
            self.lineedit.show()
            self.combo_1.show()
            self.combo_2.show()

            self.combo_1.instance.clear()
            self.combo_2.instance.clear()
            self.lineedit.label.setText("Длина сдвига:")
            self.combo_1.label.setText("Направление:")
            self.combo_2.label.setText("Заполнение:")

            self.combo_1.instance.addItem("Влево", Direction.LEFT)
            self.combo_1.instance.addItem("Вправо", Direction.RIGHT)
            self.combo_1.instance.addItem("Вверх", Direction.UP)
            self.combo_1.instance.addItem("Вниз", Direction.DOWN)

            self.combo_2.instance.addItem("Черным", FillingRule.FILL_BLACK)
            self.combo_2.instance.addItem("Зациклить", FillingRule.FILL_LOOP)
        else:
            self.combo_1.hide()
            self.combo_2.hide()
            self.lineedit.hide()

    def _on_statistic_color_correction_radiobutton_toggle(self, checked: bool):
        def _on_choose_click():
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly

            fileName, _ = QFileDialog.getOpenFileName(self, "Выберите эталонный файл", "",
                                                      "Images (*.png *.jpeg *.jpg *.bmp *.gif)", options=options)
            if fileName:
                self.statistic_color_correction_reference_pic = fileName
                self.button.instance.setText(fileName.split("/")[-1])

        if checked:
            self.button.show()
            self.button.label.setText("Эталон:")
            text = "Выбрать..." if self.statistic_color_correction_reference_pic is None else self.statistic_color_correction_reference_pic.split("/")[-1]
            self.button.instance.setText(text)
            try:
                self.button.instance.clicked.disconnect()
            except TypeError:
                pass
            self.button.instance.clicked.connect(_on_choose_click)
        else:
            self.button.hide()

    def _on_motion_blur_radiobutton_toggle(self, checked: bool):
        if checked:
            self.lineedit.show()
            self.lineedit.label.setText("Интенсивность:")
        else: self.lineedit.hide()



