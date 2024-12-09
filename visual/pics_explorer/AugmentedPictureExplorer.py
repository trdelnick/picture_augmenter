from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel

from visual.pics_explorer.PictureExplorerBase import PictureExplorerBase
from visual.menus.AugmentedFileExplorerMenu import AugmentedFileExplorerMenu


class AugmentedPictureExplorer(PictureExplorerBase):
    def __init__(self, explorer_path: str):
        super().__init__(explorer_path)

        self.is_save_dir_set = False

        self.explorer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.explorer.customContextMenuRequested.connect(self._on_custom_menu)

        self.selected_dir_label = QLabel()
        self.selected_dir_label.setText("Директория для сохранения:")

        self.selected_dir = QLabel("Не выбрано")
        self.selected_dir.setAlignment(Qt.AlignRight)
        self.selected_dir.setEnabled(False)

        self.status_bar.setLayout(QHBoxLayout())
        self.status_bar.layout().addWidget(self.selected_dir_label)
        self.status_bar.layout().addWidget(self.selected_dir)

        self.explorer.setColumnWidth(0, 300)


    def _on_change_root_open(self):
        selector = QFileDialog.getExistingDirectory(parent=None,
                                                    caption="Select Root",
                                                    directory="/",
                                                    options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.explorer.setRootIndex(self.fs_model.setRootPath(selector))
        self.explorer.viewport().update()


    def _on_custom_menu(self, point: QPoint):
        index = self.explorer.indexAt(point)
        menu = AugmentedFileExplorerMenu(index, self)
        self.explorer.viewport().update()
        menu.exec_(self.explorer.viewport().mapToGlobal(point))
