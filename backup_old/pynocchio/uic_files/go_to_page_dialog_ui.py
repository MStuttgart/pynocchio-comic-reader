

# Form implementation generated from reading ui file './forms/go_to_page_dialog.ui'
#
# Created by: PySide6 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

from . import main_window_view_rc


class Ui_GoPageDialog(object):
    def setupUi(self, GoPageDialog):
        GoPageDialog.setObjectName("GoPageDialog")
        GoPageDialog.resize(285, 514)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/edit-find.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GoPageDialog.setWindowIcon(icon)
        GoPageDialog.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        GoPageDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GoPageDialog)
        self.verticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("vertical_layout")
        self.group_box = QtWidgets.QGroupBox(GoPageDialog)
        self.group_box.setTitle("")
        self.group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.group_box.setFlat(False)
        self.group_box.setObjectName("group_box")
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.group_box)
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 9)
        self.vertical_layout_3.setSpacing(0)
        self.vertical_layout_3.setObjectName("vertical_layout_3")
        self.scroll_area = QtWidgets.QScrollArea(self.group_box)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scroll_area.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 275, 405))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_widget_contents.sizePolicy().hasHeightForWidth())
        self.scroll_area_widget_contents.setSizePolicy(sizePolicy)
        self.scroll_area_widget_contents.setObjectName(
            "scroll_area_widget_contents")
        self.horizontal_layout = QtWidgets.QHBoxLayout(
            self.scroll_area_widget_contents)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.page_label = QtWidgets.QLabel(self.scroll_area_widget_contents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.page_label.sizePolicy().hasHeightForWidth())
        self.page_label.setSizePolicy(sizePolicy)
        self.page_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.page_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.page_label.setText("")
        self.page_label.setPixmap(QtGui.QPixmap(":/icons/icons/edit-find.png"))
        self.page_label.setAlignment(QtCore.Qt.AlignCenter)
        self.page_label.setObjectName("page_label")
        self.horizontal_layout.addWidget(self.page_label)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.vertical_layout_3.addWidget(self.scroll_area)
        self.vertical_layout.addWidget(self.group_box)
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setObjectName("grid_layout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacerItem, 2, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacerItem1, 2, 0, 1, 1)
        self.spin_box_go_page = QtWidgets.QSpinBox(GoPageDialog)
        self.spin_box_go_page.setWrapping(False)
        self.spin_box_go_page.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_go_page.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spin_box_go_page.setAccelerated(True)
        self.spin_box_go_page.setCorrectionMode(
            QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.spin_box_go_page.setSuffix("")
        self.spin_box_go_page.setPrefix("")
        self.spin_box_go_page.setMinimum(1)
        self.spin_box_go_page.setSingleStep(1)
        self.spin_box_go_page.setObjectName("spin_box_go_page")
        self.grid_layout.addWidget(self.spin_box_go_page, 2, 2, 1, 1)
        self.page_label_2 = QtWidgets.QLabel(GoPageDialog)
        self.page_label_2.setObjectName("page_label_2")
        self.grid_layout.addWidget(self.page_label_2, 2, 1, 1, 1)
        self.total_page_label = QtWidgets.QLabel(GoPageDialog)
        self.total_page_label.setObjectName("total_page_label")
        self.grid_layout.addWidget(self.total_page_label, 2, 3, 1, 1)
        self.horizontal_slider = QtWidgets.QSlider(GoPageDialog)
        self.horizontal_slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.horizontal_slider.setAutoFillBackground(False)
        self.horizontal_slider.setMinimum(1)
        self.horizontal_slider.setPageStep(4)
        self.horizontal_slider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_slider.setInvertedAppearance(False)
        self.horizontal_slider.setInvertedControls(False)
        self.horizontal_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontal_slider.setTickInterval(4)
        self.horizontal_slider.setObjectName("horizontal_slider")
        self.grid_layout.addWidget(self.horizontal_slider, 3, 0, 1, 6)
        self.vertical_layout.addLayout(self.grid_layout)
        self.verticalLayout.addLayout(self.vertical_layout)
        self.buttonBox = QtWidgets.QDialogButtonBox(GoPageDialog)
        self.buttonBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonBox.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GoPageDialog)
        self.horizontal_slider.valueChanged['int'].connect(
            self.spin_box_go_page.setValue)
        self.spin_box_go_page.valueChanged['int'].connect(
            self.horizontal_slider.setValue)
        self.horizontal_slider.valueChanged['int'].connect(GoPageDialog.update)
        self.buttonBox.accepted.connect(GoPageDialog.accept)
        self.buttonBox.rejected.connect(GoPageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GoPageDialog)

    def retranslateUi(self, GoPageDialog):
        _translate = QtCore.QCoreApplication.translate
        GoPageDialog.setWindowTitle(_translate("GoPageDialog", "Go to Page"))
        self.page_label_2.setText(_translate("GoPageDialog", "Page "))
        self.total_page_label.setText(_translate("GoPageDialog", "page"))
