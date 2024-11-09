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

import QtQuick.Controls

import shared


PynocchioAutoWidthMenu {
    title: qsTranslate("HeaderBar", "&Help")

    Action {
        text: qsTranslate("HeaderBar", "&Report a bug")

        onTriggered: {
            console.log("Action about pressed")
        }
    }

    MenuSeparator { }

    Action {
        text: qsTranslate("HeaderBar", "&About Pynocchio")

        onTriggered: {
            console.log("Action 3 pressed")
        }
    }

}
