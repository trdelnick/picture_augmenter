import os.path

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QHBoxLayout, QFileDialog, QProgressBar, \
    QPushButton, QLabel

from visual.ColorDelegate import ColorDelegate

from visual.pics_explorer.PictureExplorerBase import PictureExplorerBase
from visual.menus.OriginalFileExplorerMenu import OriginalFileExplorerMenu


class OriginalPictureExplorer(PictureExplorerBase):
    def __init__(self, explorer_path: str):
        super().__init__(explorer_path)

        self.selected_inodes = set()
        self.item_delegate = ColorDelegate(selected_inodes=self.selected_inodes)
        self.explorer.setItemDelegate(self.item_delegate)

        self.explorer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.explorer.customContextMenuRequested.connect(self._on_custom_menu)

        self.progress = QProgressBar()
        self.status_bar_layout = QHBoxLayout()
        self.status_bar.setLayout(self.status_bar_layout)
        self.status_bar_layout.addWidget(self.progress)
        self.how_many_selected = QLabel("Отмечено: 0 файлов в 0 директориях")
        self.status_bar_layout.addWidget(self.how_many_selected)
        self.explorer.setColumnWidth(0, 300)

    def _on_custom_menu(self, point: QPoint):
        index = self.explorer.indexAt(point)
        menu = OriginalFileExplorerMenu(index, self)
        self.explorer.viewport().update()
        menu.exec_(self.explorer.viewport().mapToGlobal(point))


    def _on_change_root_open(self):
        selector = QFileDialog.getExistingDirectory(parent=None,
                                                    caption="Select Root",
                                                    directory="",
                                                    options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.explorer.setRootIndex(self.fs_model.setRootPath(selector))
        self.explorer.viewport().update()

    def count_selection(self):
        dirs = 0
        files = 0
        for path in self.selected_inodes:
            if os.path.isdir(path):
                dirs += 1
            else:
                files += 1
        return dirs, files
