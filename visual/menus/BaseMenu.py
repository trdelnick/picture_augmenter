import os
from math import remainder
from operator import index

from PyQt5.QtCore import QObject, QModelIndex, QFile, Qt
from PyQt5.QtWidgets import QMenu, QAction, QFileSystemModel, QTreeView, QErrorMessage, QMessageBox, QLineEdit, \
    QInputDialog

class BaseMenu(QMenu):
    def __init__(self, index: QModelIndex, fs_model: QFileSystemModel):
        super().__init__()

        self.fs_model: QFileSystemModel = fs_model
        self.index = index

        create_folder = QAction("Создать папку", self)
        self.addAction(create_folder)
        create_folder.triggered.connect(self._on_create_folder)

        if self.fs_model.fileName(index) != "":
            rename = QAction("Переименовать", self)
            self.addAction(rename)
            rename.triggered.connect(self._on_rename)

    def _on_create_folder(self):
        if self.fs_model.filePath(self.index) == "":
            path = self.fs_model.rootPath()
        else:
            path = self.fs_model.filePath(self.index)
            if not self.fs_model.isDir(self.index):
                path = self.fs_model.filePath(self.index.parent())

        new_folder_name = "NewFolder"
        if os.path.exists(path + "/" + new_folder_name):
            a = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) and name.startswith("NewFolder")]
            max_num = 1
            for name in a:
                number = name.replace("NewFolder", "")
                try:
                    max_num = max(max_num, int(number) + 1)
                except: pass
            new_folder_name = new_folder_name + str(max_num)
        os.mkdir(path + "/" + new_folder_name)

    def _on_rename(self):
        path = self.fs_model.filePath(self.index)
        old_name = path.split("/")[-1]
        text, ok_pressed = QInputDialog.getText(None, "Переименовать файл", "Имя файла:", QLineEdit.Normal, old_name)
        if ok_pressed:
            if old_name == text: return
            if os.path.exists("/".join(path.split("/")[:-1] + [text])):
                QMessageBox.critical(None, "Already exists", "Это имя уже занято")
                return
            else:
                try:
                    if "/" in text or "\\" in text:
                        raise RuntimeError()
                    os.rename(path, "/".join(path.split("/")[:-1] + [text]))
                except:
                    QMessageBox.critical(None, "Name incorrect", "Данное имя некорретно")


