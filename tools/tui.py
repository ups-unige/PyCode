from typing import Iterable
from os import curdir
from os.path import realpath
from pathlib import Path

from h5py import File

from rich.table import Table
from rich_pixels import Pixels
from textual import on
from textual.app import App
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import (
    Button, DirectoryTree, Footer, Header, Static, Tree)

import matplotlib.pyplot as plt

from pycode.experiment import PhaseInfo
from pycode.hdf5 import H5Content
from pycode.io import load_phase_from_hdf5
from pycode.operation import rasterplot_phase

# TAREA STATES
TAREA_LIST_H5 = 0
TAREA_INFO_PHASE = 1


GLOBALS = {
    'curdir': Path(curdir).absolute(),
    'curfile': None,
    'intro_shown': False,
    'tarea_state': TAREA_LIST_H5,
}

###############################################################################
#                               PYCODE STUFFS
###############################################################################


def load_phase_info(file_path: Path) -> PhaseInfo:
    phase = load_phase_from_hdf5(file_path)
    return phase.phase_info()


def rasterplot(file_path: Path):
    phase = load_phase_from_hdf5(file_path)
    for k in phase.peaks.keys():
        print(phase.peaks.get(k))
    fig, ax = plt.subplots()
    rasterplot_phase(phase, ax)
    plt.show()

###############################################################################
#                               GUI STUFFS
###############################################################################


class Intro(Screen):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.introfile = Path(realpath(__file__)[:-7] + "../images/smp.png")

    def compose(self):
        yield Static(Pixels.from_image_path(self.introfile),
                     shrink=True, classes='intro')


class PhaseTree(Tree):
    def __init__(self, content: H5Content, *kargs, **kwargs):
        super().__init__(content.name, *kargs, **kwargs)
        for analog in content.analogs:
            self.root.expand()
            analog_node = self.root.add(analog.name, expand=True)
            analog_node.collapse()
            for i in range(analog.length):
                analog_node.add_leaf(f"Channel {i}", data=(analog, i))

    def on_tree_node_selected(self, selected):
        data = selected.node.data
        if data is not None:
            plt.plot(data[0].parse_signal(data[1]))
            plt.show()


class HDF5DirectoryTree(DirectoryTree):
    def __init__(self, path, classes=""):
        super().__init__(path, classes=classes)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        ret = []
        for i, path in enumerate(paths):
            if path.is_dir() or path.suffix == '.h5':
                ret.append(path)
        return ret

    def on_directory_tree_file_selected(self, message):
        if message.path.suffix == '.h5':
            with File(message.path, 'r') as file:
                GLOBALS['curfile'] = message.path
                global text
                text = ''

                def add_text(line):
                    global text
                    text += '\n' + line
                file.visit(
                    lambda x: add_text(x))
                self.screen.get_widget_by_id('tarea').remove_children()
                self.screen.get_widget_by_id('tarea').mount(
                    PhaseTree(H5Content(message.path)))

#                self.screen.get_widget_by_id('tarea').mount(TextArea(text))


class Tui(App):
    BINDINGS = [
        ('ctrl+p', 'command_palette', 'Commands'),
        ('u', 'parent_dir', 'Parent directory'),
        ('q', 'quit', 'Quit'),
        ('f1', 'secret_option', 'HELP ME PLEASE'),
    ]

    CSS_PATH = 'root.css'

    def __init__(self):
        super().__init__()
        self.install_screen(Intro(), name='intro')

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield HDF5DirectoryTree(GLOBALS['curdir'], classes='dirtree')
        yield Vertical(id='tarea')
        with Vertical(id='controls'):
            yield Button('Open', classes='control', id='btn_open')
            yield Button('Rasterplot', classes='control', id='btn_rasterplot')
            yield Button('Open', classes='control')

    def action_parent_dir(self):
        GLOBALS['curdir'] = GLOBALS['curdir'].parent
        dt = self.query_one(DirectoryTree)
        dt.path = GLOBALS['curdir']

    def action_secret_option(self):
        if GLOBALS['intro_shown']:
            GLOBALS['intro_shown'] = False
            self.pop_screen()
        else:
            GLOBALS['intro_shown'] = True
            self.push_screen('intro')

    @on(Button.Pressed, '#btn_open')
    def btn_action_open(self):
        if GLOBALS['curfile'] is not None:
            info = load_phase_info(GLOBALS['curfile'])
            table = Table(title='Phase properties')
            table.add_column('Property')
            table.add_column('Value')
            table.add_row('Name', info.name)
            table.add_row('DIV', str(info.div))
            table.add_row('Type', str(info.phase_type))
            table.add_row('With digital', str(info.digital))
            self.screen.get_widget_by_id('tarea').remove_children()
            self.screen.get_widget_by_id('tarea').mount(Static(table))
        else:
            self.notify('You shall first select a phase file to open',
                        title='No current file',
                        severity='error')

    @on(Button.Pressed, '#btn_rasterplot')
    def btn_action_rasterplot(self):
        if GLOBALS['curfile'] is not None:
            rasterplot(GLOBALS['curfile'])
        else:
            self.notify('You shall first select a phase file to plot',
                        title='No current file',
                        severity='error')


if __name__ == "__main__":
    tui = Tui()
    tui.run()
