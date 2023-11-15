from sys import argv, exit

from qtpy.QtCore import QDir, Qt  # type: ignore
from qtpy.QtGui import QFileSystemModel  # type: ignore
from qtpy.QtWidgets import (QApplication, QPushButton,  # type: ignore
                            QSplitter, QTreeView, QVBoxLayout, QWidget)


class FileTree(QWidget):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        model = QFileSystemModel()
        model.setNameFilters(["*.h5"])
        model.setNameFilterDisables(False)
        model.setRootPath(QDir.currentPath())

        layout = QVBoxLayout()
        button = QPushButton("Parent window")
        tree = QTreeView()
        tree.setModel(model)
        tree.setRootIndex(model.index(QDir.currentPath()))
        tree.hideColumn(2)
        tree.setColumnWidth(0, 180)
        tree.setColumnWidth(1, 30)
        tree.setColumnWidth(3, 80)
        layout.addWidget(button)
        layout.addWidget(tree)
        button.clicked.connect(
            lambda: tree.setRootIndex(tree.rootIndex().parent()))
        self.setLayout(layout)


class Viewer(QWidget):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)


class Controls(QWidget):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)


class Main(QSplitter):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.setWindowTitle("Hdf5 phases explorator")
        self.setHandleWidth(1)
        self.setStyleSheet("QSplitter::handle{background-color:rgb(0, 0, 0);}")

        self.tree = FileTree()
        self.viewer = Viewer()
        self.controls = Controls()

        self.addWidget(self.tree)
        self.addWidget(self.viewer)
        self.addWidget(self.controls)


if __name__ == "__main__":
    app = QApplication(argv)
    win = Main()
    win.showMaximized()
    exit(app.exec())
