from enum import Enum

class ParentKind(str, Enum):
    """Enum for the kind of parent a widget has."""
    NOPARENT = "NoParent"
    MAYA = "Maya"
    HOUDINI = "Houdini"