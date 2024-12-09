import os.path
from PyQt5 import QtGui
from PyQt5.QtCore import  QModelIndex, Qt
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication

from visual.menus.BaseMenu import BaseMenu


class OriginalFileExplorerMenu(BaseMenu):
    def __init__(self, index: QModelIndex, picture_explorer):
        super().__init__(index, picture_explorer.fs_model)
        self.picture_explorer = picture_explorer

        self.addSeparator()

        mark_selected = QAction("Отметить", self)
        self.addAction(mark_selected)
        mark_selected.triggered.connect(self._on_select_highlighted)

        unselect_all = QAction("Сбросить все отметки", self)
        font = unselect_all.font()
        font.setBold(True)
        unselect_all.setFont(font)
        self.addAction(unselect_all)
        unselect_all.triggered.connect(self._on_unselect_all)

        unselect_highlighted = QAction("Сбросить отметки", self)
        self.addAction(unselect_highlighted)
        unselect_highlighted.triggered.connect(self._on_unselect_highlighted)

        self.addSeparator()

        change_root = QAction("Сменить корневую папку...", self)
        self.addAction(change_root)
        change_root.triggered.connect(self._on_change_root)

    def _on_select_highlighted(self):
        QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))

        def process_dir(dir_path):
            self.picture_explorer.selected_inodes.add(dir_path)
            for name in os.listdir(dir_path):
                if os.path.isdir(dir_path + "/" + name):
                    process_dir(dir_path + "/" + name)
                else:
                    ext = name.split(".")[-1]
                    if ext in ("png", "jpeg", "jpg", "bmp", "gif"):
                        self.picture_explorer.selected_inodes.add(dir_path + "/" + name)

        selected_indices = self.picture_explorer.explorer.selectedIndexes()
        for index in selected_indices:
            path = self.fs_model.filePath(index)
            if path.endswith("/"):
                path = path[:-1]
            if os.path.isdir(path):
                process_dir(path)
            else:
                ext = path.split(".")[-1]
                if ext in ("png", "jpeg", "jpg", "bmp", "gif"):
                    self.picture_explorer.selected_inodes.add(path)

        self.picture_explorer.explorer.viewport().update()

        dirs, files = self.picture_explorer.count_selection()
        self.picture_explorer.how_many_selected.setText(f"Отмечено: {files} файлов в {dirs} директориях")
        QApplication.restoreOverrideCursor()


    def _on_unselect_all(self):
        self.picture_explorer.selected_inodes.clear()
        self.picture_explorer.explorer.viewport().update()
        self.picture_explorer.how_many_selected.setText("Отмечено: 0 файлов в 0 директориях")

    def _on_unselect_highlighted(self):
        QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        def process_dir(dir_path: str):
            if dir_path in self.picture_explorer.selected_inodes:
                self.picture_explorer.selected_inodes.remove(dir_path)
            for name in os.listdir(dir_path):
                if os.path.isdir(dir_path + "/" + name):
                    process_dir(dir_path + "/" + name)
                else:
                    if dir_path + "/" + name in self.picture_explorer.selected_inodes:
                        self.picture_explorer.selected_inodes.remove(dir_path + "/" + name)

        selected_indices = self.picture_explorer.explorer.selectedIndexes()
        for index in selected_indices:
            path = self.fs_model.filePath(index)
            if path.endswith("/"):
                path = path[:-1]
            if os.path.isdir(path):
                process_dir(path)

            if path in self.picture_explorer.selected_inodes:
                self.picture_explorer.selected_inodes.remove(path)

        self.picture_explorer.explorer.clearSelection()
        self.picture_explorer.explorer.viewport().update()

        dirs, files = self.picture_explorer.count_selection()
        self.picture_explorer.how_many_selected.setText(f"Отмечено: {files} файлов в {dirs} директориях")

        QApplication.restoreOverrideCursor()

    def _on_change_root(self):
        selector = QFileDialog.getExistingDirectory(parent=None,
                                                    caption="Select Root",
                                                    directory="",
                                                    options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.picture_explorer.explorer.setRootIndex(self.fs_model.setRootPath(selector))
        self.picture_explorer.explorer.viewport().update()

