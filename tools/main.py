from datetime import datetime
from multiprocessing import Process
from os.path import getctime, getsize, realpath
from pathlib import Path
from sys import argv, exit
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from h5py import File  # type: ignore
from PySide6.QtCore import QDir, Qt, QUrl  # type: ignore
from PySide6.QtGui import (QImage, QPixmap, QStandardItem,  # type: ignore
                           QStandardItemModel)
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer  # type: ignore
from PySide6.QtWidgets import (QApplication, QCheckBox,
                               QDialog,  # type: ignore
                               QFileSystemModel, QGroupBox, QLabel,
                               QPushButton, QSplitter, QTextBrowser, QTreeView,
                               QVBoxLayout, QWidget)

from pycode.hdf5 import H5Content
from pycode.io import load_phase_from_hdf5
from pycode.operation import rasterplot_phase

# GLOBALS
ROOT = None
CURRENT_PATH = Optional[Path]
STORED_H5: Dict[Path, H5Content] = {}
MODEL = QStandardItemModel()
SIGNAL_INDEXES: Optional[Tuple[int, int]] = None


# TOO IMPORTANT STUFF
PLAYER: QMediaPlayer = QMediaPlayer()
AUDIO_OUTPUT = QAudioOutput()
PLAYER.setAudioOutput(AUDIO_OUTPUT)
MEDIA_PATH = QUrl.fromLocalFile(realpath(__file__)[:-7] + "kr.mp3")
PLAYER.setSource(MEDIA_PATH)
PLAYER.errorOccurred.connect(lambda _: print(PLAYER.errorString()))

###############################################################################
# UTILITY FUNCTIONS


def plot_signal(path: Path, indexes: Tuple[int, int]):
    content = H5Content(path)
    plt.plot(content.analogs[indexes[0]].parse_signal(indexes[1]))
    plt.show()


def plot_signal_raw(data: np.ndarray):
    plt.plot(data)
    plt.show()


def rasterplot(path: Path):
    phase = load_phase_from_hdf5(path)
    fig, ax = plt.subplots()
    rasterplot_phase(phase, ax)
    plt.show()

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
                    ROOT.controls.enable_controls_phase(False)
                    ROOT.viewer.set_h5_info(is_dir=True)
                    ROOT.viewer.toggle_tree(False)
                else:
                    file = CURRENT_PATH
                    info_h5 = self.InfoH5(
                        file.name, f'{ "%.2f" % (getsize(file) / 1024 / 1024) } MB', datetime.fromtimestamp(getctime(file)).strftime('%Y-%m-%d %H:%M:%S'))
                    ROOT.controls.enable_controls_phase(True)
                    ROOT.viewer.set_h5_info(info_h5=info_h5)
                ROOT.controls.enable_controls_signal(False)

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
        self.tree.selectionChanged = self.check_tree_item

    def check_tree_item(self, selected, _deselected):
        selection = selected.data()
        if selection is not None:
            data = MODEL.itemFromIndex(selection.indexes()[0]).data()
            if data is not None:
                ROOT.controls.enable_controls_signal(True, indexes=data)
            else:
                ROOT.controls.enable_controls_signal(False)
        else:
            ROOT.controls.enable_controls_signal(False)

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

        MODEL.clear()
        MODEL.setHorizontalHeaderItem(0, QStandardItem("Data"))
        analog_streams_item = QStandardItem("Analog Streams")
        analog_streams_item.setEditable(False)
        MODEL.appendRow(analog_streams_item)
        for i, analog in enumerate(content.analogs):
            analog_item = QStandardItem(analog.name)
            analog_item.setEditable(False)
            sorted_channels = sorted(
                analog.info_channels, key=lambda x: int(x.label))
            for j, channel in enumerate(sorted_channels):
                # actual index of the relative channeldata is at channel.channel_id
                channel_item = QStandardItem(f"Channel {int(channel.label)}")
                channel_item.setData((i, int(channel.channel_id)))
                channel_item.setEditable(False)
                analog_item.appendRow(channel_item)

            analog_streams_item.appendRow(analog_item)
        self.tree.setModel(MODEL)
        self.toggle_tree()


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

        plots_group = QGroupBox(title="Plotting")
        plots_layout = QVBoxLayout()
        plots_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_rasterplot = QPushButton("Rasterplot")
        plots_layout.addWidget(self.btn_rasterplot)
        self.btn_rasterplot.clicked.connect(
            lambda _: Process(target=rasterplot, args=(CURRENT_PATH, )).start())

        signals_group = QGroupBox(title="Signals")
        signals_layout = QVBoxLayout()
        signals_group.setLayout(signals_layout)
        self.btn_plot_signal = QPushButton("Plot Signal")
        self.btn_plot_signal.clicked.connect(
            lambda _: plot_signal_raw(
                STORED_H5[CURRENT_PATH].analogs[SIGNAL_INDEXES[0]].parse_signal(SIGNAL_INDEXES[1])))
        signals_layout.addWidget(self.btn_plot_signal)

        self.plot_events_in_signal = QCheckBox(text="Include events")
        signals_layout.addWidget(self.plot_events_in_signal)

        plots_layout.addWidget(signals_group)

        plots_group.setLayout(plots_layout)

        layout.addWidget(plots_group)

        self.setLayout(layout)
        self.enable_controls_phase(False)

    def enable_controls_phase(self, value: bool):
        self.btn_content.setEnabled(value)
        self.btn_tree.setEnabled(value)
        self.btn_rasterplot.setEnabled(value)

    def enable_controls_signal(self, value: bool, indexes=None):
        self.setEnabled(value)
        global SIGNAL_INDEXES
        SIGNAL_INDEXES = indexes


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
        PLAYER.play()

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
