# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'thumbnails.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QDockWidget,
    QFrame,
    QLayout,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_Thumbnails(object):
    def setupUi(self, Thumbnails):
        if not Thumbnails.objectName():
            Thumbnails.setObjectName("Thumbnails")
        Thumbnails.resize(659, 577)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Thumbnails.sizePolicy().hasHeightForWidth())
        Thumbnails.setSizePolicy(sizePolicy)
        Thumbnails.setFloating(False)
        Thumbnails.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.dockWidgetContents = QScrollArea()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setFrameShape(QFrame.Shape.NoFrame)
        self.dockWidgetContents.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.dockWidgetContents.setWidgetResizable(False)
        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(0, 0, 120, 120))
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.dockWidgetContents.setWidget(self.widget)
        Thumbnails.setWidget(self.dockWidgetContents)

        self.retranslateUi(Thumbnails)

        QMetaObject.connectSlotsByName(Thumbnails)

    # setupUi

    def retranslateUi(self, Thumbnails):
        Thumbnails.setWindowTitle(QCoreApplication.translate("Thumbnails", "Thumbnails", None))

    # retranslateUi
