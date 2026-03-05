try:
    from PySide6.QtCore import QObject, Signal
except ImportError:
    try:
        from PyQt6.QtCore import QObject, pyqtSignal as Signal
    except ImportError:
        try:
            from PyQt5.QtCore import QObject, pyqtSignal as Signal
        except ImportError:
            raise ImportError(
                "qtzmq requires PySide6, PyQt6, or PyQt5."
            )