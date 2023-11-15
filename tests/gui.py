from qtpy.QtWidgets import (QApplication, QTreeView,
                            QVBoxLayout, QPushButton, QWidget)
from qtpy.QtCore import QDir
from qtpy.QtGui import QFileSystemModel

app = QApplication([])

# Create a QWidget which will be our main window
window = QWidget()

# Create a QVBoxLayout which will contain our QTreeView and QPushButton
layout = QVBoxLayout()

model = QFileSystemModel()
model.setRootPath(QDir.currentPath())

tree = QTreeView()
tree.setModel(model)
tree.setRootIndex(model.index(QDir.currentPath()))

# Create a QPushButton
button = QPushButton("Go to parent directory")
button.clicked.connect(lambda: tree.setRootIndex(tree.rootIndex().parent()))

# Add the QTreeView and QPushButton to the layout
layout.addWidget(tree)
layout.addWidget(button)

# Set the layout of the main window
window.setLayout(layout)

window.show()
app.exec()
