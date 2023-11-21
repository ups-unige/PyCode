from datetime import datetime
from os.path import getctime, getsize, realpath
from pathlib import Path
from sys import argv, exit
from typing import Dict, Optional

from h5py import File  # type: ignore
from PySide6.QtCore import QDir, Qt, QUrl  # type: ignore
from PySide6.QtGui import QImage, QPixmap  # type: ignore
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer  # type: ignore
from PySide6.QtWidgets import (QApplication, QDialog, QFileSystemModel, QGroupBox,  # type: ignore
                               QLabel, QPushButton, QSplitter, QTextBrowser,
                               QTreeView, QVBoxLayout, QWidget)

from pycode.hdf5 import H5Content

# GLOBALS
ROOT = None
CURRENT_PATH = Optional[Path]
STORED_H5: Dict[Path, H5Content] = {}
PLAYER: QMediaPlayer = QMediaPlayer()
AUDIO_OUTPUT = QAudioOutput()
PLAYER.setAudioOutput(AUDIO_OUTPUT)
MEDIA_PATH = QUrl.fromLocalFile(realpath(__file__)[:-7] + "kr.mp3")
PLAYER.setSource(MEDIA_PATH)
PLAYER.errorOccurred.connect(lambda _: print("here\n" + PLAYER.errorString()))

###############################################################################
# FILE TREE


class FileTree(QWidget):
    class InfoH5:
        def __init__(self, name, size, date):
            self.name = name
            self.size = size
            self.date = date

    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        model = QFileSystemModel()
        model.setNameFilters(["*.h5"])
        model.setNameFilterDisables(False)
        model.setRootPath(QDir.currentPath())

        layout = QVBoxLayout()
        button = QPushButton("Parent window")

        def file_selection_changed(new_file, old_file):
            '''
            Here it is the action made when a file in the explorer is selected
            It should set the appropriate controls if the file is an h5 and
            disable them if it is a directory. In addition it should update
            the info panel of the h5 file if one it's selected.
            '''
            count = new_file.count()
            if count > 0:
                model_index = new_file.indexes()[0]
                # is_dir = model.isDir(model_index)
                path = model.filePath(model_index)
                global CURRENT_PATH
                CURRENT_PATH = Path(path)
                if CURRENT_PATH.is_dir():
                    ROOT.controls.enable_controls(False)
                    ROOT.viewer.set_h5_info(is_dir=True)
                    ROOT.viewer.toggle_tree(False)
                else:
                    file = CURRENT_PATH
                    info_h5 = self.InfoH5(
                        file.name, f'{ "%.2f" % (getsize(file) / 1024 / 1024) } MB', datetime.fromtimestamp(getctime(file)).strftime('%Y-%m-%d %H:%M:%S'))
                    ROOT.controls.enable_controls(True)
                    ROOT.viewer.set_h5_info(info_h5=info_h5)

        tree = QTreeView()
        tree.selectionChanged = file_selection_changed
        tree.setModel(model)
        tree.setRootIndex(model.index(QDir.currentPath()))
        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)
        tree.setColumnWidth(0, 200)
        layout.addWidget(button)
        layout.addWidget(tree)
        button.clicked.connect(
            lambda: tree.setRootIndex(tree.rootIndex().parent()))
        self.setLayout(layout)

###############################################################################
# VIEWER SECTION


class Viewer(QWidget):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # basic file info
        self.info = QLabel()
        layout.addWidget(self.info)

        # h5 content
        self.content = QTextBrowser()
        layout.addWidget(self.content)
        self.content.setVisible(False)

        # h5 tree
        self.tree = QTreeView()
        layout.addWidget(self.tree)
        self.tree.setVisible(False)

    def toggle_content(self, value=True):
        self.content.setVisible(value)
        self.tree.setVisible(False)

    def toggle_tree(self, value=True):
        self.content.setVisible(False)
        self.tree.setVisible(value)

    def set_h5_info(self, info_h5: Optional[FileTree] = None, is_dir=False):
        if is_dir:
            self.info.clear()
        else:
            if info_h5 is not None:
                content = f'''
File name:      {info_h5.name}
File size:      {info_h5.size}
Creation date:  {info_h5.date}
                '''
                self.info.setText(content)

    def get_h5_content(self, file_path: Path):
        with File(file_path, 'r') as file:
            global text
            text = ''  # type: ignore

            def add_text(line):
                global text
                text += line + '\n'

            file.visit(lambda x: add_text(x))
            self.content.setText(text)  # type: ignore
        self.toggle_content()

    def populate_tree(self, file_path: Path):
        content = None
        if STORED_H5.get(file_path) is not None:
            content = STORED_H5[file_path]
        else:
            content = H5Content(file_path)
            STORED_H5[file_path] = content

        self.toggle_tree()
        print(content.analogs)


###############################################################################
# CONTROLS SECTION


class Controls(QWidget):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        layout = QVBoxLayout()

        inspect_group = QGroupBox(title="Inspect")
        inspect_layout = QVBoxLayout()
        inspect_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_tree = QPushButton("Show data tree")
        self.btn_tree.clicked.connect(
            lambda _: ROOT.viewer.populate_tree(CURRENT_PATH))
        self.btn_content = QPushButton("Show content")
        self.btn_content.clicked.connect(
            lambda _: ROOT.viewer.get_h5_content(CURRENT_PATH))

        inspect_layout.addWidget(self.btn_content)
        inspect_layout.addWidget(self.btn_tree)
        inspect_group.setLayout(inspect_layout)

        layout.addWidget(inspect_group)

        analisys_group = QGroupBox(title="Analisys")
        analisys_layout = QVBoxLayout()
        analisys_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_rasterplot = QPushButton("Rasterplot")

        analisys_layout.addWidget(self.btn_rasterplot)
        analisys_group.setLayout(analisys_layout)

        layout.addWidget(analisys_group)

        self.setLayout(layout)
        self.enable_controls(False)

    def enable_controls(self, value: bool):
        self.btn_content.setEnabled(value)
        self.btn_tree.setEnabled(value)
        self.btn_rasterplot.setEnabled(value)


###############################################################################
# BONUS SECTION

class Info(QDialog):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        image = QLabel()
        image.setScaledContents(True)
        image_path = realpath(__file__)[:-7] + "sm.jpg"
        image.setPixmap(QPixmap.fromImage(QImage(image_path)))
        layout = QVBoxLayout()
        layout.addWidget(image)
        self.setLayout(layout)
        print(PLAYER.mediaStatus())
        PLAYER.play()
        print(PLAYER.playbackState())

    def closeEvent(self, a):
        PLAYER.stop()

###############################################################################
# MAIN WINDOW


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

    def resizeEvent(self, a):
        min_width = 800
        min_height = 600
        tree_min_size = 300
        tree_max_size = 400
        tree_parts = 3
        controls_min_size = 100
        controls_max_size = 300
        controls_parts = 3

        cur_geometry = self.geometry()
        w = cur_geometry.width()
        tree_size = w // 10 * tree_parts
        if tree_size > tree_max_size:
            tree_size = tree_max_size
        elif tree_size < tree_min_size:
            tree_size = tree_min_size
        controls_size = w // 10 * controls_parts
        if controls_size > controls_max_size:
            controls_size = controls_max_size
        elif controls_size < controls_min_size:
            controls_size = controls_min_size
        if cur_geometry.width() < (tree_size + controls_size):
            cur_geometry.setWidth(tree_size + controls_size)
            self.setGeometry(cur_geometry)

        viewer_size = cur_geometry.width() - tree_size - controls_size
        self.setSizes([tree_size, viewer_size, controls_size])

        if cur_geometry.width() < min_width:
            cur_geometry.setWidth(min_width)
            self.setGeometry(cur_geometry)
        if cur_geometry.height() < min_height:
            cur_geometry.setHeight(min_height)
            self.setGeometry(cur_geometry)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F1:
            self.info = Info()
            self.info.showMaximized()


if __name__ == "__main__":
    app = QApplication(argv)
    win = Main()
    ROOT = win
    win.showMaximized()
    exit(app.exec())
