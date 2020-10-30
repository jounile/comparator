#!/usr/bin/env python3.6
import os
import sys
from photoshop import Session
from PIL import Image, ImageChops
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QMainWindow, QApplication, QScrollArea, QAction, QLabel, QShortcut, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QPushButton, QFileSystemModel, QComboBox, QButtonGroup
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from datetime import datetime

class ComparatorApp(QMainWindow):

    def __init__(self): 
        super().__init__()

        self.activeContext = "Example"
        self.activeVersionPrev = ""
        self.activeVersionNext = ""
        self.versionPrevDir = "Version1"
        self.versionNextDir = "Version2"
        self.defaultLayerComp1 = "Layer Comp 1.png"
        self.get_menu()
        self.statusBar()
        self.setWindowTitle("ComparatorApp")
        self.load_example()
        self.create_dropdowns()
        self.update_context_dropdown()
        self.create_labels()
        self.update_prev_folder_dropdown()
        self.update_next_folder_dropdown()
        self.update_prev_layercomp_dropdown()
        self.update_next_layercomp_dropdown()
        self.create_buttons()
        self.create_button_group()
        self.create_buttons_layout_row1()
        self.create_buttons_layout_row2()
        self.create_shortcuts()
        self.create_pixmap()
        self.update_window_size()
        self.create_layout()
        self.create_widgets()
        self.create_signals()

    def load_example(self):
        versionPrevPath = os.path.join(self.getContextDir(), self.versionPrevDir)
        versionNextPath = os.path.join(self.getContextDir(), self.versionNextDir)
        image1path = os.path.join(versionPrevPath, self.defaultLayerComp1)
        image2path = os.path.join(versionNextPath, self.defaultLayerComp1)

        self.image1 = None
        self.image2 = None
        self.image3 = None

        image1 = Image.open(image1path).convert('RGB')
        image2 = Image.open(image2path).convert('RGB')
        image3 = self.get_difference(image1, image2)

        self.qim1 = ImageQt(image1)
        self.qim2 = ImageQt(image2)
        self.qim3 = ImageQt(image3)

    def prevBtn_pressed(self):
        self.label.setPixmap(self.pixmap1)

    def nextBtn_pressed(self):
        self.label.setPixmap(self.pixmap2)

    def diffBtn_pressed(self):
        self.image3 = self.get_difference(self.image1, self.image2)
        self.qim3 = ImageQt(self.image3)
        self.pixmap3 = QPixmap.fromImage(self.qim3)
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
        self.shortcut_enter = QShortcut(Qt.Key_Return, self)
        self.shortcut_enter.activated.connect(self.diffBtn_pressed)

    def create_buttons(self):
        self.prevBtn = QPushButton("Previous", self)
        self.prevBtn.setCheckable(True)
        self.nextBtn = QPushButton("Next", self)
        self.nextBtn.setCheckable(True)
        self.diffBtn = QPushButton("Diff", self)
        self.diffBtn.setCheckable(True)

    def create_button_group(self):
        self.btnGroup = QButtonGroup()
        self.btnGroup.addButton(self.prevBtn)
        self.btnGroup.addButton(self.nextBtn)
        self.btnGroup.addButton(self.diffBtn)

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

    def create_pixmap(self):
        self.pixmap1 = QPixmap.fromImage(self.qim1)
        self.pixmap2 = QPixmap.fromImage(self.qim2)
        self.pixmap3 = QPixmap.fromImage(self.qim3)

    def get_menu(self):
        openPsdAction = QAction("&Extract PSD", self)
        openPsdAction.triggered.connect(self.extractLayerCompositionsFromPsd)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openPsdAction)

    def setContext(self):
        self.activeContext = self.contextDropdown.currentText()
        self.update_prev_folder_dropdown()
        self.update_next_folder_dropdown()

    def setVersionPrev(self):
        self.activeVersionPrev = self.folderDropdownPrevious.currentText()
        self.versionPrevDir = os.path.join(self.getContextDir(), self.activeVersionPrev)
        self.update_prev_layercomp_dropdown()

    def setVersionNext(self):
        self.activeVersionNext = self.folderDropdownNext.currentText()
        self.versionNextDir = os.path.join(self.getContextDir(), self.activeVersionNext)
        self.update_next_layercomp_dropdown()

    def setLayerCompPrev(self):
        self.activeLayerCompPrev = self.layerCompsDropdownPrevious.currentText()
        if self.activeLayerCompPrev:
            imagePath1 = os.path.join(self.versionPrevDir, self.activeLayerCompPrev)
            self.image1 = Image.open(imagePath1).convert('RGB')
            self.pixmap1 = QPixmap(imagePath1)
            self.label.setPixmap(self.pixmap1)

    def setLayerCompNext(self):
        self.activeLayerCompNext = self.layerCompsDropdownNext.currentText()
        if self.activeLayerCompNext:
            imagePath2 = os.path.join(self.versionNextDir, self.activeLayerCompNext)
            self.image2 = Image.open(imagePath2).convert('RGB')
            self.pixmap2 = QPixmap(imagePath2)
            self.label.setPixmap(self.pixmap2)

    def update_context_dropdown(self):
        dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
        self.contextDropdown.clear()
        self.contextDropdown.addItems(dirs)

    def create_dropdowns(self):
        self.contextDropdown = QComboBox()
        self.contextDropdown.currentIndexChanged.connect(self.setContext)
        self.folderDropdownPrevious = QComboBox()
        self.folderDropdownPrevious.currentIndexChanged.connect(self.setVersionPrev)
        self.folderDropdownNext = QComboBox()
        self.folderDropdownNext.currentIndexChanged.connect(self.setVersionNext)
        self.layerCompsDropdownPrevious = QComboBox()
        self.layerCompsDropdownPrevious.currentIndexChanged.connect(self.setLayerCompPrev)
        self.layerCompsDropdownNext = QComboBox()
        self.layerCompsDropdownNext.currentIndexChanged.connect(self.setLayerCompNext)
        self.folderDropdownLayout = QHBoxLayout()
        self.folderDropdownLayout.addWidget(self.folderDropdownPrevious)
        self.folderDropdownLayout.addWidget(self.folderDropdownNext)
        self.layerCompsDropdownLayout = QHBoxLayout()
        self.layerCompsDropdownLayout.addWidget(self.layerCompsDropdownPrevious)
        self.layerCompsDropdownLayout.addWidget(self.layerCompsDropdownNext)

    def update_prev_folder_dropdown(self):
        if self.activeContext:
            dirs = [name for name in os.listdir(self.activeContext)]
            self.folderDropdownPrevious.clear()
            self.folderDropdownPrevious.addItems(dirs)
            self.folderDropdownPrevious.setCurrentIndex(0)

    def update_next_folder_dropdown(self):
        if self.activeContext:
            dirs = [name for name in os.listdir(self.activeContext)]
            self.folderDropdownNext.clear()
            self.folderDropdownNext.addItems(dirs)
            self.folderDropdownNext.setCurrentIndex(1)

    def update_prev_layercomp_dropdown(self):
        layerComps = []
        self.layerCompsDropdownPrevious.clear()
        if self.activeVersionPrev:
            dirPath = os.path.join(os.getcwd(), self.activeContext)
            dirPath = os.path.join(dirPath, self.activeVersionPrev)
            for layerComp in os.listdir(dirPath):
                layerComps.append(layerComp)
            self.layerCompsDropdownPrevious.addItems(layerComps)

    def update_next_layercomp_dropdown(self):
        layerComps = []
        self.layerCompsDropdownNext.clear()
        if self.activeVersionNext:
            dirPath = os.path.join(os.getcwd(), self.activeContext)
            dirPath = os.path.join(dirPath, self.activeVersionNext)
            for layerComp in os.listdir(dirPath):
                layerComps.append(layerComp)
            self.layerCompsDropdownNext.addItems(layerComps)

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.contextDropdown)
        self.layout.addLayout(self.folderDropdownLayout)
        self.layout.addLayout(self.layerCompsDropdownLayout)
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

    def extractLayerCompositionsFromPsd(self):
        fileName = self.openFileDialog()
        if fileName:
            print("Start extracting")
            with Session(fileName, action="open") as ps:
                fileName = os.path.basename(fileName)
                print("Opening PSD file", fileName)
                fileName , extension = os.path.splitext(fileName)
                if not os.path.exists(os.path.join(os.getcwd(), self.activeContext)):
                    os.mkdir(self.activeContext)
                extractDir = os.path.join(self.getContextDir(), fileName + "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                os.mkdir(extractDir)
                doc = ps.active_document
                options = ps.PNGSaveOptions()
                for layerComp in doc.layerComps:
                    layerComp.apply()
                    extractPath = os.path.join(extractDir, f"{layerComp.name}.png")
                    print("Extract ", extractPath)
                    doc.saveAs(extractPath, options, True)
            print("Finished extracting")

    def getContextDir(self):
        cwd = os.getcwd()
        return os.path.join(cwd, self.activeContext)

    def openFileDialog(self):    
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", filter="*.png *.psd", options=options)
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