import os.path
import cv2
from PyQt5.QtCore import QItemSelectionModel, QTimer
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, \
    QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt

from augmenter.BaseAugmenter import BaseAugmenter
from augmenter.DenoiserBlur import DenoiserBlur
from augmenter.DenoiserGauss import DenoiserGauss
from augmenter.Equalizer import Equalizer
from augmenter.MotionBlur import MotionBlur
from augmenter.MoveAugmentor import MoveAugmentor
from augmenter.Noiser import Noiser
from augmenter.StatisticColorCorrector import StatisticColorCorrector
from visual.AugmentAlgorithmsWrapper import AugmentAlgorithmsWrapper
from visual.pics_explorer.AugmentedPictureExplorer import AugmentedPictureExplorer
from visual.pics_explorer.OriginalPictureExplorer import OriginalPictureExplorer

ROOT_PATH = ""
SAVE_ROOT_PATH = ""


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.original_pics = OriginalPictureExplorer(ROOT_PATH)
        self.augmented_pics = AugmentedPictureExplorer(SAVE_ROOT_PATH)
        self.augmented_pics.is_greyscale_checkbox.hide()

        # pictures
        self.pics_layout = QVBoxLayout()
        self.pics_layout.addWidget(self.original_pics)

        delimiter = QPushButton("")
        delimiter.setDisabled(True)
        delimiter.setFixedHeight(3)
        delimiter.setStyleSheet("background-color: #239923; border: none")

        self.pics_layout.addWidget(delimiter)
        self.pics_layout.addWidget(self.augmented_pics)

        self.pics_widget = QWidget()
        self.pics_widget.setLayout(self.pics_layout)

        # settings

        self.settings_layout = QVBoxLayout()

        self.transform_button = QPushButton("Преобразовать отмеченное")
        self.transform_radio = AugmentAlgorithmsWrapper()

        self.transform_button.clicked.connect(self._on_transform)

        self.settings_layout.addStretch(10)
        self.settings_layout.addWidget(self.transform_button)
        self.settings_layout.addStretch(1)
        self.settings_layout.addWidget(self.transform_radio)
        self.settings_layout.addStretch(10)

        self.settings_widget = QWidget()
        self.settings_widget.setFixedWidth(350)
        self.settings_widget.setLayout(self.settings_layout)
        self.settings_widget_wrapper = QWidget()
        self.settings_widget_layout = QHBoxLayout()
        self.settings_widget_wrapper.setLayout(self.settings_widget_layout)
        self.settings_widget_layout.addStretch(1)
        self.settings_widget_layout.addWidget(self.settings_widget)
        self.settings_widget_layout.addStretch(1)

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.settings_widget_wrapper)

        delimiter = QPushButton("")
        delimiter.setDisabled(True)
        delimiter.setFixedWidth(3)
        delimiter.setStyleSheet("background-color: #239923; border: none")

        self.main_splitter.addWidget(delimiter)
        self.main_splitter.addWidget(self.pics_widget)

        self.main_splitter.setSizes([200, 1, 1000])

        self.setCentralWidget(self.main_splitter)
        self.resize(998, 878)
        self.showMaximized()



    def transform(self, augmenter: BaseAugmenter, file_label:str = "augmented"):
        selected_paths = self.original_pics.selected_inodes
        overall_paths = len(selected_paths)
        progress_step = 100 / overall_paths
        curr_progress = 0
        for path in selected_paths:
            if os.path.isdir(path):
                continue
            import cv2
            pic = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            aug_pic = augmenter.apply(pic)
            name = path.split("/")[-1].split(".")
            ext = name[-1]
            filename = ".".join(name[:-1])
            aug_path = f"{self.augmented_pics.selected_dir.text()}/{filename}_{file_label}.{ext}"
            cv2.imwrite(aug_path, aug_pic)

            curr_progress += progress_step
            self.original_pics.progress.setValue(int(curr_progress))

        index = self.augmented_pics.fs_model.index(aug_path)
        self.augmented_pics.pics_explorer_double_clicked(index)
        self.augmented_pics.explorer.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)

        self.original_pics.progress.setValue(100)
        self.original_pics.progress.setValue(-1)


    def _on_transform(self):
        if not self.augmented_pics.is_save_dir_set:
            self.augmented_pics.status_bar.setStyleSheet("background-color: red")
            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(lambda : self.augmented_pics.status_bar.setStyleSheet(""))
            self.timer.start()

            QMessageBox.warning(self, "Ошибка", "Директория для сохранения должна быть задана")
            return

        _, files = self.original_pics.count_selection()
        if files == 0:
            self.original_pics.how_many_selected.setStyleSheet("background-color: red")
            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(lambda : self.original_pics.how_many_selected.setStyleSheet(""))
            self.timer.start()
            QMessageBox.warning(self, "Ошибка", "Файлы для аугментации не отмечены")
            return

        if self.transform_radio.button_group.checkedButton() == self.transform_radio.add_noise_radiobutton:
            try:
                data = float(self.transform_radio.lineedit.instance.text())
                self.transform(Noiser(data), f"noised-{data}")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректные данные")

        elif self.transform_radio.button_group.checkedButton() == self.transform_radio.blur_mean_radiobutton:
            try:
                data = int(self.transform_radio.lineedit.instance.text())
                self.transform(DenoiserBlur(data), f"blur-{data}")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректные данные")

        elif self.transform_radio.button_group.checkedButton() == self.transform_radio.blur_gauss_radiobutton:
            try:
                data = float(self.transform_radio.lineedit.instance.text())
                self.transform(DenoiserGauss(data), f"gauss-{data}")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректные данные")

        elif self.transform_radio.button_group.checkedButton() == self.transform_radio.equalize_radiobutton:
            self.transform(Equalizer(), f"equalize")

        elif self.transform_radio.button_group.checkedButton() == self.transform_radio.statistic_color_correction_radiobutton:
            if self.transform_radio.statistic_color_correction_reference_pic is not None:
                source_pic = cv2.imread(self.transform_radio.statistic_color_correction_reference_pic)
                self.transform(StatisticColorCorrector(source_pic), f"statistic")
            else:
                QMessageBox.warning(self, "Ошибка", "Введите корректные данные")

        elif self.transform_radio.button_group.checkedButton() == self.transform_radio.move_radiobutton:
            try:
                how_many_pix = int(self.transform_radio.lineedit.instance.text())
                direction = self.transform_radio.combo_1.instance.itemData(self.transform_radio.combo_1.instance.currentIndex())
                filling = self.transform_radio.combo_2.instance.itemData(self.transform_radio.combo_2.instance.currentIndex())
                self.transform(MoveAugmentor(how_many_pix, direction, filling), f"move-{direction.name}-{how_many_pix}-{filling.name}")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректные данные")
            except RuntimeError as e:
                QMessageBox.warning(self, "Ошибка", str(e))


        elif self.transform_radio.button_group.checkedButton() == self.transform_radio.motion_blur_radiobutton:
            try:
                how_many_pix = int(self.transform_radio.lineedit.instance.text())
                self.transform(MotionBlur(how_many_pix), f"motion-{how_many_pix}")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректные данные")

        else:
            QMessageBox.warning(self, "Ошибка", "Алгоритм не выбран")
            return


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
