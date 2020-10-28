#!/usr/bin/env python3.6
import sys 
from PIL import Image, ImageChops
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QMainWindow, QApplication, QScrollArea, QAction, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

class ComparatorApp(QMainWindow):

    def __init__(self): 
        super().__init__() 

        self.get_menu()
        self.statusBar()

        self.setWindowTitle("ComparatorApp")
       
        self.create_labels()
       
        # Paths of two image frames
        image1path = './image1.jpg'
        image2path = './image2.jpg'
       
        self.image1 = None
        self.image2 = None
        self.image3 = None

        image1 = Image.open(image1path).convert('RGB')
        image2 = Image.open(image2path).convert('RGB')
        image3 = self.get_difference(image1, image2)
       
        # Convert images
        self.qim1 = ImageQt(image1)
        self.qim2 = ImageQt(image2)
        self.qim3 = ImageQt(image3)
       
        self.create_pixmap()
        self.add_image_to_label()
        self.update_window_size()
        self.create_layout()
        self.create_widgets()
   
    def create_labels(self):
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)

    def add_image_to_label(self):
        self.label1.setPixmap(self.pixmap1)
        self.label2.setPixmap(self.pixmap2)
        self.label3.setPixmap(self.pixmap3)

    def create_pixmap(self):
        self.pixmap1 = QPixmap.fromImage(self.qim1)
        self.pixmap2 = QPixmap.fromImage(self.qim2)
        self.pixmap3 = QPixmap.fromImage(self.qim3)
        
    def get_menu(self):
        openPreviousAction = QAction("&Open previous", self)
        openPreviousAction.setStatusTip('Open previous image')
        openPreviousAction.triggered.connect(self.loadPreviousDelivery)

        openNewAction = QAction("&Open latest", self)
        openNewAction.setStatusTip('Open new image')
        openNewAction.triggered.connect(self.loadNewDelivery)
       
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openPreviousAction)
        fileMenu.addAction(openNewAction)

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        
    def create_widgets(self):
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        self.show()
        
    def get_difference(self, image1, image2):
        return ImageChops.difference(image1, image2)
    
    def update_window_size(self):
        self.setGeometry(0, 0, self.pixmap1.width(), self.pixmap1.height())
        
    def loadPreviousDelivery(self):
        fileName = self.openFileDialog()
        if fileName:
            print(fileName)
            self.image1 = Image.open(fileName).convert('RGB')
            self.pixmap1 = QPixmap(fileName)
            self.label1.setPixmap(self.pixmap1)
            
    def loadNewDelivery(self):
        fileName = self.openFileDialog()
        if fileName:
            print(fileName)
            self.image2 = Image.open(fileName).convert('RGB')
            self.pixmap2 = QPixmap(fileName)
            self.label2.setPixmap(self.pixmap2)
            self.update_diff()
            
    def update_diff(self):
        self.image3 = self.get_difference(self.image1, self.image2)
        self.qim3 = ImageQt(self.image3)
        self.pixmap3 = QPixmap.fromImage(self.qim3)
        if not self.pixmap3.isNull():
            self.label3.setPixmap(self.pixmap3)

    def openFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", filter="*.png", options=options)
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