/*
Copyright

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls
import QtCore
import QtQuick.Dialogs
import app

import bridge

ApplicationWindow {
    id: root

    width: 1280
    height: 720
    flags: Qt.FramelessWindowHint | Qt.Window
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red

    LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    Bridge {
      id: bridge
    }

    PynocchioMainPage {
        appWindow: _shared

        anchors {
            fill: root.contentItem
            margins: _private.windowBorder
        }
    }

    Component.onCompleted: {
        // load language from settings
        // Qt.uiLanguage = ...
    }

    QtObject {
        id: _private  // Implementation details not exposed to child items

        readonly property bool maximized: root.visibility === Window.Maximized
        readonly property bool fullscreen: root.visibility === Window.FullScreen
        readonly property int windowBorder: fullscreen || maximized ? 0 : 1
    }

    QtObject {
        id: _shared  // Properties and functions exposed to child items

        readonly property var visibility: root.visibility

        function startSystemMove() {
            root.startSystemMove()
        }

        function showMinimized() {
            root.showMinimized()
        }

        function showMaximized() {
            root.showMaximized()
        }

        function showNormal() {
            root.showNormal()
        }

        function close() {
            root.close()
        }
    }



    FileDialog {
      id: openDialog
      fileMode: FileDialog.OpenFile
      selectedNameFilter.index: 0
      nameFilters: ["Comic Files (*.cbr *.cbz)", "Compact files (*.zip *.rar)"]
      currentFolder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
      onAccepted: {
        //console.log(fileDialog.fileUrls)
        bridge.openComic(selectedFile)
      }
    }



}
