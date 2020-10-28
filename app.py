#!/usr/bin/env python3.6
import sys 
from PIL import Image, ImageChops
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QMainWindow, QApplication, QScrollArea, QAction, QLabel, QShortcut, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

class ComparatorApp(QMainWindow): 

    def __init__(self): 
        super().__init__()

        self.get_menu()
        self.statusBar()

        self.setWindowTitle("ComparatorApp")

        self.create_labels()
        self.create_buttons()
        self.create_buttons_layout_row1()
        self.create_buttons_layout_row2()
        self.create_shortcuts()

        image1path = './image1.jpg'
        image2path = './image2.jpg'

        self.image1 = None
        self.image2 = None
        self.image3 = None

        image1 = Image.open(image1path).convert('RGB')
        image2 = Image.open(image2path).convert('RGB')
        image3 = self.get_difference(image1, image2)

        self.qim1 = ImageQt(image1)
        self.qim2 = ImageQt(image2)
        self.qim3 = ImageQt(image3)

        self.create_pixmap()
        self.add_image_to_label()
        self.update_window_size()
        self.create_layout()
        self.create_widgets()
        self.create_signals()

    def prevBtn_pressed(self):
        self.label.setPixmap(self.pixmap1)

    def nextBtn_pressed(self):
        self.label.setPixmap(self.pixmap2)

    def diffBtn_pressed(self):
        self.label.setPixmap(self.pixmap3)

    def create_signals(self):
        self.prevBtn.clicked.connect(self.prevBtn_pressed)
        self.nextBtn.clicked.connect(self.nextBtn_pressed)
        self.diffBtn.clicked.connect(self.diffBtn_pressed)

    def create_shortcuts(self):
        self.shortcut_left = QShortcut(Qt.Key_Left, self)
        self.shortcut_left.activated.connect(self.prevBtn_pressed)
        self.shortcut_right = QShortcut(Qt.Key_Right, self)
        self.shortcut_right.activated.connect(self.nextBtn_pressed)
        self.shortcut_down = QShortcut(Qt.Key_Down, self)
        self.shortcut_down.activated.connect(self.diffBtn_pressed)

    def create_buttons(self):
        self.prevBtn = QPushButton("Previous", self)
        self.nextBtn = QPushButton("Next", self)
        self.diffBtn = QPushButton("Diff", self)

    def create_buttons_layout_row1(self):
        self.btnLayoutRow1 = QHBoxLayout()
        self.btnLayoutRow1.addWidget(self.prevBtn)
        self.btnLayoutRow1.addWidget(self.nextBtn)
        self.btnLayoutRow1.setContentsMargins(0,0,0,0)
        self.btnLayoutRow1.setSpacing(10)

    def create_buttons_layout_row2(self):
        self.btnLayoutRow2 = QHBoxLayout()
        self.btnLayoutRow2.addWidget(self.diffBtn)
        self.btnLayoutRow2.setContentsMargins(0,0,0,0)
        self.btnLayoutRow2.setSpacing(10)

    def create_labels(self):
        self.label = QLabel(self)

    def add_image_to_label(self):
        self.label.setPixmap(self.pixmap1)

    def create_pixmap(self):
        self.pixmap1 = QPixmap.fromImage(self.qim1)
        self.pixmap2 = QPixmap.fromImage(self.qim2)
        self.pixmap3 = QPixmap.fromImage(self.qim3)

    def get_menu(self):
        openPreviousAction = QAction("&Open previous", self)
        openPreviousAction.triggered.connect(self.loadPreviousDelivery)

        openNewAction = QAction("&Open latest", self)
        openNewAction.triggered.connect(self.loadNewDelivery)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openPreviousAction)
        fileMenu.addAction(openNewAction)

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.btnLayoutRow1)
        self.layout.addLayout(self.btnLayoutRow2)
        self.layout.addWidget(self.label)

    def create_widgets(self):
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()

    def get_difference(self, image1, image2):
        return ImageChops.difference(image1, image2)
        #return ImageChops.blend(image1, image2, 0.5)
        #return ImageChops.add_modulo(image1, image2)
        #return ImageChops.add(image1, image2, 1.0, 0)
        #return ImageChops.darker(image1, image2)
        #return ImageChops.lighter(image1, image2)
        #return ImageChops.multiply(image1, image2)
        #return ImageChops.screen(image1, image2)
        #return ImageChops.subtract(image, image2)
        #return ImageChops.subtract_modulo(image1, image2)

    def update_window_size(self):
        self.setGeometry(0, 0, self.pixmap1.width(), self.pixmap1.height() + 100)

    def loadPreviousDelivery(self):
        fileName = self.openFileDialog()
        if fileName:
            print(fileName)
            self.image1 = Image.open(fileName).convert('RGB')
            self.pixmap1 = QPixmap(fileName)
            self.pixmap2 = QPixmap()
            self.pixmap3 = QPixmap()
            self.label.setPixmap(self.pixmap1)

    def loadNewDelivery(self):
        fileName = self.openFileDialog()
        if fileName:
            print(fileName)
            self.image2 = Image.open(fileName).convert('RGB')
            self.pixmap2 = QPixmap(fileName)
            self.update_diff()

    def update_diff(self):
        self.image3 = self.get_difference(self.image1, self.image2)
        self.qim3 = ImageQt(self.image3)
        self.pixmap3 = QPixmap.fromImage(self.qim3)

    def openFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", filter="*.png *.jpg", options=options)
        return fileName

    def closeApplication(self):
        sys.exit()

def main():
    App = QApplication(sys.argv) 
    comparator = ComparatorApp()
    comparator.show()
    sys.exit(App.exec())

if __name__ == '__main__': 
    main()