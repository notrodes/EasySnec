import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QObject, Property, Signal

import serial.tools.list_ports

class SiHandler(QObject):
    
    _serial_ports = []
    _current_port = None
    
    dataChanged = Signal()
    
    def __init__(self):
        super().__init__()
        for port in serial.tools.list_ports.comports():
            self._serial_ports.append(port.device)
    
    @Property(list, notify=dataChanged)
    def serial_ports(self):
        return self._serial_ports

if __name__ == "__main__":
    si = SiHandler()
    
    app = QGuiApplication()
    view = QQuickView()

    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setInitialProperties({"siHandler": si, "serialPorts": si.serial_ports})

    # Load the QML file
    # Add the current directory to the import paths and load the main module.
    view.engine().addImportPath(sys.path[0])
    view.loadFromModule("App", "Main")
    
    # Show the window
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    # execute and cleanup
    ex = app.exec()
    del view
    sys.exit(ex)