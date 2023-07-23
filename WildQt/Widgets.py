

class CreateWidget():
    """Creates a custom widget.
    
    Creates a custom widget that can be added to a layout.
    Extended usage gives properties, multiple widget addition, and customizing layout.
    
    ---
    Public Functions:
        - addWidget(): Adds a widget to the layout.
        - addWidgets(): Adds multiple widgets to the layout.
    ---
    Properties:
        - widget: The primary widget item.
    """

    def __init__(self, layout_type=QVBoxLayout, style=QFrame.Box, spacing=5, alignment=None):
        """Creates a custom widget.
        
        ---
        Args:
            - layout_type (QLayout): The layout type to use. Defaults to QVBoxLayout.
            - style (QFrame): The style of the widget. Defaults to QFrame.Box.
            - spacing (int): The spacing between widgets. Defaults to 5.
            - alignment (Qt.Alignment): The alignment of the widget. Defaults to None.
        """

        self._layout = layout_type()

        if alignment is not None:
            self._layout.setAlignment(alignment)

        spacing = 5 if style is QFrame.Box else spacing
        self._layout.setMargin(spacing)        

        self._widget = QFrame()
        self._widget.setFrameShape(style)
        self._widget.setLayout(self._layout)

        custom_policy = QSizePolicy()
        custom_policy.setVerticalPolicy(QSizePolicy.Preferred)
        
        custom_policy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)
        self._widget.setSizePolicy(custom_policy)
        self._widget.setGeometry(0, 0, 20, 20)

        css = """
            QFrame {
                border: 2px solid #323436;
            }
        """

        self._widget.setStyleSheet(css)
        self.resize()

    def addWidget(self, widget):
        # type: (QWidget) -> None
        """Adds a widget to the layout.

        ---
        Args:
            - widget (QWidget): The widget to add.
        """

        self._layout.addWidget(widget)
        self.resize()

    def addWidgets(self, *widgets, layout=None):
        # type: (list[QWidget], list[tuple(int, int)]) -> None
        """Adds multiple widgets to the layout.

        ---
        Args:
            - widgets (list[QWidget]): A list of QWidget items to add.
            - layout (list[tuple(int, int)]): A list of 2D tuples, indicating layout directions to use with QGridLayout. Defaults to None
        """

        for ii, widget in enumerate(widgets):
            if type(self._layout) == QGridLayout and layout is not None:
                self._layout.addWidget(widget, *layout[ii])
                continue
            self._layout.addWidget(widget)
        self.resize()

    def resize(self):
        # type: () -> None
        """Resizes the widget to fit the contents.
        """

        self._widget.setMinimumHeight(self._widget.sizeHint().height())

    @property
    def widget(self):
        # type: () -> QWidget
        """Returns the base widget object.

        ---
        Returns:
            - widget (QWidget): The base widget object.
        """

        return self._widget
    
    @property
    def layout(self):
        # type: () -> QLayout
        """Returns the base layout object.
        
        ---
        Returns:
            - layout (QLayout): The base layout object.
        """

        return self._layout



"""A reimplementation, modified of the collapsible header widget.
Original comes from Chris Zurbrigg.

"""

class CollapsibleHeader(QWidget):
    """A collapsible header widget.
    
    ---
    Attributes:
        - COLLAPSED_PIXMAP (QPixmap): The collapsed pixmap.
        - EXPANDED_PIXMAP (QPixmap): The expanded pixmap.
    ---
    Signals and Slots:
        - clicked (Signal): The clicked signal.
    """
    
    COLLAPSED_PIXMAP = None
    EXPANDED_PIXMAP = None

    clicked = Signal()
    
    def __init__(self, title="", parent=None, expandable=True):
        # type: (str, QWidget, bool) -> None
        """Creates a collapsible header.
        
        ---
        Args:
            - title (str): The title of the header.
            - parent (QWidget): The parent widget.
            - expandable (bool): If true, the header is expandable.
        """

        super(CollapsibleHeader, self).__init__(parent)

        try:
            self.COLLAPSED_PIXMAP = QPixmap(":teRightArrow.png")
            self.EXPANDED_PIXMAP = QPixmap(":teDownArrow.png")
        except:
            pass
        
        self.setAutoFillBackground(True)
        self.setBackgroundColour(None)
        
        self.isExpandable = expandable
        
        if self.isExpandable:
            self.icon_Label = QLabel()
            self.icon_Label.setFixedWidth(self.COLLAPSED_PIXMAP.width())
        
        self.lbl_Title = QLabel()
        self.lbl_Title.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.lay_main = QHBoxLayout(self)
        self.lay_main.setContentsMargins(4, 4, 4, 4)
        if self.isExpandable:
            self.lay_main.addWidget(self.icon_Label)
        self.lay_main.addWidget(self.lbl_Title)
        self.setMinimumHeight(20)
        
        self.setText(title)
        self.setExpanded(True)
        
    def setText(self, text):
        # type: (str) -> None
        """Sets the text of the header.

        ---
        Args:
            - text (str): The text to set the header to.
        """

        self.lbl_Title.setText("<b>{0}</b>".format(text))
        
    def setBackgroundColour(self, colour):
        # type: (QColor) -> None
        """Sets the background colour of the header.
        
        ---
        Args:
            - colour (QColor): The colour to set the header to.
        """

        if not colour:
            colour = QPushButton().palette().color(QPalette.Button)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, colour)
        self.setPalette(palette)
        
    def isExpanded(self):
        # type: () -> bool
        """Returns whether the header is expanded or not.
        
        ---
        Returns:
            - bool: True if expanded, False if collapsed.
        """

        return self._expanded
        
    def setExpanded(self, expanded):
        # type: (bool) -> None
        """Sets the header to expanded or collapsed.
        
        ---
        Args:
            - expanded (bool): If true, the header is expanded.
        """

        self._expanded = expanded
        
        if self.isExpandable:
            if(self._expanded):
                self.icon_Label.setPixmap(self.EXPANDED_PIXMAP)
            else:
                self.icon_Label.setPixmap(self.COLLAPSED_PIXMAP)
            
    def mouseReleaseEvent(self, event):
        # type: (QMouseEvent) -> None
        """Calls the clicked signal.
        
        ---
        Args:
            - event (QMouseEvent): The mouse event.
        """

        self.clicked.emit()


class CollapsibleWidget(QFrame):
    def __init__(self, text="", headerEnabled=True, layout=None, widgetToAdd=None, parent=None):
        # type: (str, bool, QLayout, QWidget, QWidget) -> None
        """Creates a collapsible widget.

        ---
        Args:
            - text (str): The text to display in the header.
            - headerEnabled (bool): If true, the header is enabled.
            - layout (QLayout): The layout to use.
            - widgetToAdd (QWidget): The widget to add to the collapsible widget.
            - parent (QWidget): The parent widget.
        """

        super(CollapsibleWidget, self).__init__(parent)
        self.initalize(text=text, headerEnabled=headerEnabled)

        if widgetToAdd:
            self.addWidget(widgetToAdd)

        if layout is not None:
            layout.addWidget(self)

    def initalize(self, text="", headerEnabled=True):
        # type: (str, bool) -> None
        """Initializes the collapsible widget.
        
        ---
        Args:
            - text (str): The text to display in the header.
            - headerEnabled (bool): If true, the header is enabled. 
        """

        self.header_wdg = CollapsibleHeader(text, expandable=headerEnabled)
        if headerEnabled:
            self.header_wdg.clicked.connect(self.onHeaderClicked)
        
        self.body_wdg = QWidget()
        
        self.body_layout = QVBoxLayout(self.body_wdg)
        self.body_layout.setContentsMargins(4, 2, 4, 2)
        self.body_layout.setSpacing(3)
        
        self.lay_main = QVBoxLayout(self)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.lay_main.addWidget(self.header_wdg)
        self.lay_main.addWidget(self.body_wdg)
        self.lay_main.setAlignment(Qt.AlignTop)
        
        self.setExpanded(True)

    def addWidget(self, widget):
        # type: (QWidget) -> None
        """Adds a widget to the collapsible widget.
        
        ---
        Args:
            - widget (QWidget): The widget to add.
        """

        self.body_layout.addWidget(widget)
        widget.move(0,0)
        self.setHeight(widget.minimumHeight())

    def addLayout(self, layout):
        """Adds a layout to the collapsible widget.
        
        ---
        Args:
            - layout (QLayout): The layout to add.
        """

        self.body_layout.addLayout(layout)

    def onHeaderClicked(self):
        # type: () -> None
        """Called when the header is clicked."""

        self.setExpanded(not self.header_wdg.isExpanded())
    
    def setExpanded(self, expanded):
        # type: (bool) -> None
        """Sets the collapsible widget to expanded or collapsed.
        
        ---
        Args:
            - expanded (bool): If true, the widget is expanded. 
        """

        self.header_wdg.setExpanded(expanded)
        self.body_wdg.setVisible(expanded)

    def setHeaderBackgroundColour(self, colour):
        # type: (QColor) -> None
        """Sets the background colour of the header.
        
        ---
        Args:
            - colour (QColor): The colour to set the header to.
        """

        self.header_wdg.setBackgroundColour(colour)
    
    def setHeight(self, height):
        """Sets the minimum height of the collapsible widget.
        
        ---
        Args:
            - height (int): The height to set the widget to. 
        """
        # pass
        self.body_wdg.setMinimumHeight(height)


class ClickableLabel(QLabel):
    """Creates a clickable label widget.
    Inherits from QLabel.

    ---
    Signals:
        - clicked: Emits when the label is clicked.
    """

    clicked = Signal()
    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        
    def mousePressEvent(self, event):
        self.clicked.emit()


class DirectoryTextWidget(QWidget):
    """Creates a widget with a label, text input, and button.
    Links the button to a folder dialog, which the output will then be set to the text input.
    
    ---
    Public Functions:
        - text(): Returns the text of the QLineEdit.
        - setText(): Sets the text of the QLineEdit.
    """

    def __init__(self, label="", default_value="", dialog_label="Navigate to directory...", layout=None, parent=None):
        # type: (str, str, str, QLayout, QWidget) -> None
        """Creates a widget with a label, text input, and button.
        """
        super(DirectoryTextWidget, self).__init__(parent)
        self.initalize(label, default_value)
        self.connectWidgets()

        self._dialog_label = dialog_label
        
        if layout is not None:
            layout.addWidget(self)

    def initalize(self, label, default_value):
        # type: (str, str) -> None
        """Initializes the widget.
        """
        layout = QHBoxLayout(self)
        layout.setMargin(0)

        if label != "":
            _label = QLabel(label)
            _label.setFrameStyle( QFrame.NoFrame)
            layout.addWidget(_label)

        self._text = QLineEdit(default_value)
        layout.addWidget(self._text)

        self._button = QPushButton("...")
        self._button.setMaximumWidth(30)
        self._button.setMinimumWidth(30)
        layout.addWidget(self._button)

        self.setLayout(layout)

    def connectWidgets(self):
        # type: () -> None
        """Connects widgets to functions.
        """
        self._button.clicked.connect(self.getDirectory)

    def getDirectory(self):
        """Event driven function to create a folder dialog search for the cloth setup parent folder."""
        resp = QFileDialog.getExistingDirectory(self, self._dialog_label)
        if resp is not None and resp != "":
            self._text.setText(resp)

    def text(self):
        # type: () -> str
        """Returns the text of the QLineEdit.
        """
        return self._text.text()

    def setText(self, val):
        # type: (str) -> None
        """Sets the text of the QLineEdit.
        """
        self._text.setText(val)


class ColourPicker(QWidget):
    """Creates a colour picker widget for Maya.
    
    ---
    Public Functions:
        - getHSV(): Returns the current colour in HSV.
        - getRGB(): Returns the current colour in RGB.
        - getHex(): Returns the current colour in Hex.
        - setHex(): Sets the current colour from a Hex value.
        - remapRGB(): Remaps the RGB values to 0-255.
    """

    colour_changing = Signal(list)
    colour_changed = Signal(list)

    def __init__(self, text="", clickable_swatch=True, clipboard=True, refresh=True, saturation_slider=True, parent=None):
        # type: (str, bool, bool, bool, bool, QWidget) -> None
        """Creates a colour picker widget for Maya.\n
        ---
        Args:
            - text (str): The text to display next to the colour picker.
            - clickable_swatch (bool): If true, the swatch is clickable.
            - clipboard (bool): If true, the clipboard button is visible.
            - refresh (bool): If true, the refresh button is visible.
            - saturation_slider (bool): If true, the saturation slider is visible.
            - parent (QWidget): The parent widget.
        """
        super(ColourPicker, self).__init__(parent)
        css = """
        QLabel {
                border: 0;
            }
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignRight)
        

        self.rgb_value = LAQtUi_utils.LAMColour([1.0, 1.0, 1.0, 1.0])
        self.lbl_display = QLabel(text)
        # self.lbl_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_display.setStyleSheet(css)

        self.lbl = ClickableLabel()
        self.lbl.setFixedSize(50, 20)

        if clickable_swatch:
            self.lbl.setFixedSize(100, 20)
            self.lbl.clicked.connect(self.evntPickColour)

        self.txt_hex = QLineEdit()
        self.txt_hex.setMaximumWidth(99999)
        # if not clickable_swatch and not clipboard:
                # self.txt_hex.setMaximumWidth(500)
            # if not refresh and not saturation_slider:
            # self.txt_hex.setMaximumWidth(100)
        
        self.txt_hex.textEdited.connect(self.evntHexChanged)
        self.txt_hex.editingFinished.connect(self.updateColour)

        path = os.path.dirname(os.path.realpath(__file__))
        pixmap_clipboard = QIcon(QPixmap(os.path.join(path, "icons/Bootstrap_clipboard2-x.svg")))
        pixmap_refresh = QIcon(QPixmap(os.path.join(path, "icons/arrow-clockwise.svg")))

        self.btn_clipboard = QPushButton("") #TODO - Implement clipboard copy
        self.btn_clipboard.setToolTip("Paste from clipboard.")
        self.btn_clipboard.setMaximumWidth(25)
        self.btn_clipboard.setIcon(pixmap_clipboard)
        self.btn_clipboard.setIconSize(pixmap_clipboard.actualSize(QSize(15, 15)))
        self.btn_clipboard.clicked.connect(self.evntClipboard)

        self.btn_reset = QPushButton("") #TODO - Implement clipboard copy
        self.btn_reset.setToolTip("Reset the value.")
        self.btn_reset.setMaximumWidth(25)
        self.btn_reset.setIcon(pixmap_refresh)
        self.btn_reset.setIconSize(pixmap_refresh.actualSize(QSize(15, 15)))
        self.btn_reset.clicked.connect(lambda: self.updateColour())

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.evntSlider)
        self.slider.sliderReleased.connect(self.updateColour)

        optional_ui_items = [(self.btn_clipboard, clipboard), (self.btn_reset, refresh), (self.slider, saturation_slider)]
        total_ui_items = [self.lbl, self.txt_hex] #lbl_display, 
        total_ui_items.extend([x for x, y in optional_ui_items if y]) 
         #, self.btn_clipboard, self.btn_reset, self.slider]

        for item in total_ui_items: #, self.slider]:
            layout.addWidget(item)

        layout.setStretch(4, 1)
        self.setLayout(layout)
        self.setStyleSheet(css)
        self.updateColour()

    def getDisplayLabel(self):
        return self.lbl_display

    def evntClipboard(self):
        text = QApplication.clipboard().text()
        text = text.strip().lower()
        
        self.rgb_value.set(text, colour_space=LAQtUi_utils.Colour.HEX)
        self.updateColour()


    def evntPickColour(self):
        current_colour = self.getRGB()

        cmds.colorEditor(rgb=tuple(current_colour[0:3]))
        if cmds.colorEditor(query=True, result=True):
            picked_colour = cmds.colorEditor(query=True, rgb=True)
            self.rgb_value.set(picked_colour, colour_space=LAQtUi_utils.Colour.RGB)
            self.updateColour()
        
    def evntSlider(self):
        c_colour = self.rgb_value.get(colour_space=LAQtUi_utils.Colour.HSV)
        c_colour[2] = self.slider.value() * 0.01

        self.rgb_value.set(c_colour, colour_space=LAQtUi_utils.Colour.HSV)
        self.updateColour(slide=False)

    def evntHexChanged(self):
        hex_val = self.txt_hex.text()
        if len(hex_val) == 6:
            self.rgb_value.set(hex_val, colour_space=LAQtUi_utils.Colour.HEX)
            self.updateColour(hex=False)

    def updateColour(self, hex=True, slide=True):
        # Please note, that the style sheet cannot render values over 255, doing so returns a random colour.
        self.lbl.setStyleSheet("background-color: #{}".format(self.rgb_value.get(LAQtUi_utils.Colour.HEX)))
        self.colour_changing.emit(self.rgb_value.get(colour_space=LAQtUi_utils.Colour.RGB))
        if hex:
            self.setHex()
        if slide:
            self.slider.blockSignals(True)
            self.slider.setValue(self.getHSV()[2] * 100)
            self.slider.blockSignals(False)

        if hex and slide:
            self.colour_changed.emit(self.rgb_value.get(colour_space=LAQtUi_utils.Colour.RGB))

    def getHSV(self):
        return self.rgb_value.get(colour_space=LAQtUi_utils.Colour.HSV)
    
    def getRGB(self):
        return self.rgb_value.get()
    
    def getHex(self):
        rgb = self.getRGB()
        return "{:02x}{:02x}{:02x}".format(int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0))
    
    def setHex(self, hex_val=None):
        hex_val = hex_val if hex_val else self.rgb_value.get(colour_space=LAQtUi_utils.Colour.HEX)
        self.txt_hex.blockSignals(True)
        self.txt_hex.setText(hex_val)
        self.txt_hex.blockSignals(False)
        if len(hex_val) == 6:
            self.rgb_value.set(hex_val, colour_space=LAQtUi_utils.Colour.HEX)
    
    def remapRGB(self, rgb):
        return [int(x * 255.0) for x in rgb]
    
    @property
    def colour(self):
        return self.rgb_value.get(colour_space=LAQtUi_utils.Colour.RGB)
    
    @colour.setter
    def colour(self, colour):
        self.rgb_value.set(colour, colour_space=LAQtUi_utils.Colour.RGB)
        self.updateColour()
    

## Decorators

class QHLine(QFrame):
    """Creates a horizontal line widget for display purposes.
    """
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    """Creates a vertical line widget for display purposes.
    """
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
