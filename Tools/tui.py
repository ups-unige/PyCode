from typing import Iterable
from os import curdir
from pathlib import Path
from textual.app import App
from textual.widgets import DirectoryTree, Footer, Header


GLOBALS = {
    'curdir': Path(curdir).absolute(),
}


class HDF5DirectoryTree(DirectoryTree):
    def __init__(self, path):
        super().__init__(path)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        ret = []
        for path in paths:
            if path.is_dir() or path.suffix == '.h5':
                ret.append(path)
        return ret


class Tui(App):
    BINDINGS = [
        ('ctrl+p', 'command_palette', 'Commands'),
        ('u', 'parent_dir', 'Parent directory'),
        ('q', 'quit', 'Quit'),
    ]

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield HDF5DirectoryTree(GLOBALS['curdir'])

    def action_parent_dir(self):
        GLOBALS['curdir'] = GLOBALS['curdir'].parent
        dt = self.query_one(DirectoryTree)
        dt.path = GLOBALS['curdir']


if __name__ == "__main__":
    tui = Tui()
    tui.run()
