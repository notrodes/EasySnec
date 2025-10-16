import QtQuick
import QtQuick.Controls

Page {
    width: 640
    height: 480
    id: main

    required property var siHandler
    required property list<string> serialPorts
    property string selectedPort

    header: Label {
        color: "#15af15"
        text: qsTr("EasySnec")
        font.pointSize: 17
        font.bold: true
        font.family: "Arial"
        renderType: Text.NativeRendering
        horizontalAlignment: Text.AlignHCenter
        padding: 10
    }

    Rectangle {
        id: root
        width: parent.width
        height: parent.height

        Image {
            id: image
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: root
            // source: "./logo.png"
            opacity: 0.5
        }

        ComboBox {
            id: portpicker
            anchors.fill: root
            anchors.margins: 25
            model: main.siHandler.serial_ports
            onActivated: {
                main.selectedPort = main.siHandler.serial_ports[currentIndex]
                print(main.siHandler.serial_ports[currentIndex])
            }
        }


    }
}
