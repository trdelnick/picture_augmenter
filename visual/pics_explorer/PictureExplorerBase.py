
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QSplitter, QFileSystemModel, QHBoxLayout, QLabel, QCheckBox, QVBoxLayout, QWidget


class PictureExplorerBase(QSplitter):
    def __init__(self, explorer_path: str):
        super().__init__(Qt.Horizontal)
        self.open_picture_path = ""

        self.explorer = QtWidgets.QTreeView()
        self.fs_model = QFileSystemModel()
        self.fs_model.setNameFilters(["*.png", "*.jpeg", "*.jpg", "*.bmp", "*.gif"])
        self.fs_model.setNameFilterDisables(False)

        self.explorer.setModel(self.fs_model)
        self.explorer.setRootIndex(self.fs_model.setRootPath(explorer_path))
        self.explorer.doubleClicked.connect(self.pics_explorer_double_clicked)
        self.explorer.setSelectionMode(QtWidgets.QTreeView.ExtendedSelection)
        self.explorer.setSelectionBehavior(QtWidgets.QTreeView.SelectRows)

        self.is_greyscale_checkbox = QCheckBox()
        self.is_greyscale_checkbox.setText("Черно-белый фильтр")
        self.is_greyscale_checkbox.setChecked(False)
        self.is_greyscale_checkbox.clicked.connect(self._on_grey_checkbox_click)

        self.is_greyscale_checkbox_wrapper = QWidget()
        self.is_greyscale_checkbox_layout = QHBoxLayout()
        self.is_greyscale_checkbox_wrapper.setLayout(self.is_greyscale_checkbox_layout)
        self.is_greyscale_checkbox_layout.addStretch(1)
        self.is_greyscale_checkbox_layout.addWidget(self.is_greyscale_checkbox)
        self.is_greyscale_checkbox_layout.addStretch(1)


        self.pics_displayer = QLabel()
        self.pic_and_checkbox_widget = QWidget()

        self.pics_displayer_layout = QHBoxLayout()
        self.pic_and_checkbox_layout = QVBoxLayout()
        self.pic_and_checkbox_layout.addWidget(self.pics_displayer)
        self.pic_and_checkbox_layout.addStretch(1)
        self.pic_and_checkbox_layout.addWidget(self.is_greyscale_checkbox_wrapper)
        self.pic_and_checkbox_widget.setLayout(self.pic_and_checkbox_layout)

        self.pics_displayer_layout.addStretch()
        self.pics_displayer_layout.addWidget(self.pic_and_checkbox_widget)
        self.pics_displayer_layout.addStretch()

        self.pics_displayer_layout_wrapper = QtWidgets.QWidget()
        self.pics_displayer_layout_wrapper.setLayout(self.pics_displayer_layout)
        self.pics_displayer_layout_wrapper.setMinimumWidth(200)
        self.pics_displayer_layout_wrapper.setMinimumHeight(200)

        self.explorer_bar_widget = QWidget()
        self.explorer_layout = QVBoxLayout()
        self.explorer_bar_widget.setLayout(self.explorer_layout)
        self.status_bar = QWidget()
        self.explorer_layout.addWidget(self.explorer)
        self.explorer_layout.addWidget(self.status_bar)

        self.addWidget(self.explorer_bar_widget)
        self.addWidget(self.pics_displayer_layout_wrapper)


    def prepare_picture(self, path):
        size = self.pics_displayer_layout_wrapper.size()
        ratio = (size.height() - 100) / (size.width() - 100)
        pic = QImage(path)
        if pic.height() > pic.width() * ratio:
            pic = pic.scaledToHeight(size.height() - 100)
        else:
            pic = pic.scaledToWidth(size.width() - 100)
        if self.is_greyscale_checkbox.isChecked():
            pic = pic.convertToFormat(QImage.Format_Grayscale8)
        return pic

    def pics_explorer_double_clicked(self, index: QModelIndex):
        path = self.fs_model.filePath(index)
        self.open_picture_path = path
        if self.fs_model.fileInfo(index).suffix() in ("png", "jpeg", "jpg", "bmp", "gif"):
            self.pics_displayer.setPixmap(QPixmap.fromImage(self.prepare_picture(path)))

    def _on_grey_checkbox_click(self, checkbox_about_to_become: bool):
        if self.open_picture_path == "":
            return
        self.pics_displayer.setPixmap(QPixmap.fromImage(self.prepare_picture(self.open_picture_path)))