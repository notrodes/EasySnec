// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQml

ApplicationWindow {
    id: root

    // ------- Program State! TODO: Replace with a "Model" / big object that holds all the data
    // debug value
    property var currTime: '1'

    // all available ports (possibly filtered)
    property var portOptions: []
    // selected port (this is outgoing)
    property var currPort: 'test'

    // RESULTS
    property var result_status: false
    property var result_string: "You did it!" 

    property var image_path: "./resources/glassy-smiley-late.png"

    // ------- Program State!

    visible: true
    width: 640
    height: 480

    header: Label {
        color: "#15af15"
        text: root.currTime
        font.pointSize: 17
        font.bold: true
        font.family: "Arial"
        renderType: Text.NativeRendering
        horizontalAlignment: Text.AlignHCenter
        padding: 10
    }
    StackLayout {
        anchors.fill: parent
        
        Page {
            id: runPage

            ColumnLayout{
                anchors.fill: parent

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "#ff0000"
                    Image {
                        id: image
                        fillMode: Image.PreserveAspectFit
                        // anchors.centerIn: root
                        anchors.fill:parent

                        source: root.image_path
                    }
                }

                Label {
                    color: "#15af15"
                    text: "1234"
                    font.pointSize: 17
                    font.bold: true
                    font.family: "Arial"
                    renderType: Text.NativeRendering
                    horizontalAlignment: Text.AlignHCenter
                    padding: 10

                    background: Rectangle {
                        anchors.fill: parent
                        color: "#333333"
                    }
                }
                Label {
                    color: "#15af15"
                    text: "567"
                    font.pointSize: 17
                    font.bold: true
                    font.family: "Arial"
                    renderType: Text.NativeRendering
                    horizontalAlignment: Text.AlignHCenter
                    padding: 10
                }
                // Label {
                //     color: "#15af15"
                //     // text: root.cardReading
                //     font.pointSize: 17
                //     font.bold: true
                //     font.family: "Arial"
                //     renderType: Text.NativeRendering
                //     horizontalAlignment: Text.AlignHCenter
                //     padding: 10
                // }
            }
        }
    }
    // what does this do?
    // NumberAnimation {
    //     id: anim
    //     running: true
    //     target: view
    //     property: "contentY"
    //     duration: 500
    // }
}
