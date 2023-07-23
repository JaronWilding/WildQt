"""This file contains custom window creation functions for WildQt.
"""

__author__ = "Jaron Wilding"
__license__ = "GPLv3"
__maintainer__ = "Jaron Wilding"
__version__ = "0.0.1"
__status__ = "Development"

# Python imports
import os
import sys

## PySide imports
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QPushButton, QLabel, QLineEdit, QFileDialog, QSlider
from PySide2.QtWidgets import QSizePolicy, QScrollArea, QLayout, QVBoxLayout, QHBoxLayout, QGridLayout

# Python 2/3 compatibility
if sys.version_info.major >= 3:
    long = int

class MainWindow(QMainWindow):
    """Creates a UI.

    Creates a base UI class that can be inherited from within the Maya environment.
    
    ---
    Functions:
        - createWidgets()
        - connectWidgets()
        - center()
    """
    
    def __init__(self, name="BaseUI"):
        """Creates the main window ui.\n
        ---
        Args:
            - name (str): The name of the UI. Must be unique, as it will kill all existing items.
            - parent (QWidget): The parent widget. Defaults to Maya's main window.
        """
        self.resolve(name)
        super(MainWindow, self).__init__(self._parent)
        self.setObjectName(name)
        
        self.createWidgets()
        self.connectWidgets()
        
        if isinstance(QMainWindow, self.__class__.__base__):
            self.showWindow()

        return None
    
    def resolve(self, name):
        # type: (str) -> None
        # Check Running in Maya
        self._parent = None
        self._app = None
        if os.path.splitext(os.path.basename(sys.executable))[0] in ("maya", "mayabatch", "mayapy", "mayapy2"):
            # Kill the window if it exists
            import maya.cmds as cmds
            if cmds.window(name, exists=True):
                cmds.deleteUI(name)

            from shiboken2 import wrapInstance # type: ignore
            import maya.OpenMayaUI as omui # type: ignore
            main_window_ptr = omui.MQtUtil.mainWindow()
            if main_window_ptr:
                self._parent = wrapInstance(long(main_window_ptr), QWidget)
            return
        self._app = QApplication(sys.argv)
        

    @property    
    def app(self):
        # type: () -> QApplication
        """Returns the QApplication instance."""
        return self._app
            
    def createWidgets(self):
        """Creates the initial layout for the UI. Reimplement this function with super as a starting point."""

        self.body_widget = QFrame()

        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(4, 2, 4, 2)
        self.body_layout.setSpacing(3)
        self.body_layout.setAlignment(Qt.AlignTop)

        # Create a scroll area, so when dialog is shrunk, it won't crush the rest.
        body_scroll_area = QScrollArea()

        body_scroll_area.setFrameShape(QFrame.NoFrame)
        body_scroll_area.setWidgetResizable(True)
        body_scroll_area.setWidget(self.body_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(body_scroll_area)
        
        self.setCentralWidget(body_scroll_area)

    def connectWidgets(self):
        """Connects widgets to functions. Reimplement this function with super as a starting point."""
        raise NotImplementedError("connectWidgets() must be implemented in subclass.")
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
