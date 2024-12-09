from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QAction, QFileDialog

from visual.menus.BaseMenu import BaseMenu


class AugmentedFileExplorerMenu(BaseMenu):
    def __init__(self, index: QModelIndex, picture_explorer):
        super().__init__(index, picture_explorer.fs_model)
        self.picture_explorer = picture_explorer

        if self.fs_model.fileName(index) != "":
            if self.fs_model.isDir(index):
                select_folder = QAction("Сохранять сюда", self)
                self.addSeparator()
                self.addAction(select_folder)
                select_folder.triggered.connect(self._on_select_to_save)

        self.addSeparator()

        change_root = QAction("Сменить корневую папку...", self)
        self.addAction(change_root)
        change_root.triggered.connect(self._on_change_root)

    def _on_select_to_save(self):
        path = self.fs_model.filePath(self.index)
        self.picture_explorer.selected_dir.setText(path)
        self.picture_explorer.is_save_dir_set = True

    def _on_change_root(self):
        selector = QFileDialog.getExistingDirectory(parent=None,
                                                    caption="Select Root",
                                                    directory="",
                                                    options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.picture_explorer.explorer.setRootIndex(self.fs_model.setRootPath(selector))
        self.picture_explorer.explorer.viewport().update()
