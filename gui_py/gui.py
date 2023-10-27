from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import perceptron
class Window (QWidget):
    def __init__(self):
        self.descriptionWindowLocation_Y = 0
        self.descriptionWindowLocation_X = 0
        self.windowWidth = 0
        self.windowHeight = 0
        self.descriptionImgButton = ""
        self.descriptionExitButton = ""
        self.descriptionWindowTitle = ""
        super(Window, self).__init__()
        self.initUI()
        self.show()
        self.selected_file = None

    def initUI(self):
        self.descriptionImgButton = "Upload image"
        self.descriptionWindowTitle = "Image Recognition API made by Mateusz Rosa"
        self.descriptionExitButton = "Exit"
        self.descriptionLoadCNN_Sequential = "Sequential CNN Analysis"
        self.imageNotExist_warning = "Image is not uploaded!"

        self.descriptionWindowLocation_X = 50
        self.descriptionWindowLocation_Y = 50
        self.windowWidth = 500
        self.windowHeight = 500

        self.setWindowTitle(self.descriptionWindowTitle)
        self.setGeometry(self.descriptionWindowLocation_X, self.descriptionWindowLocation_Y, self.windowWidth, self.windowHeight)

        layout = QVBoxLayout()

        self.imgButton = QPushButton(self.descriptionImgButton, self)
        self.exitButton = QPushButton(self.descriptionExitButton, self)
        self.loadCNN_Sequential = QPushButton(self.descriptionLoadCNN_Sequential, self)

        layout.addWidget(self.imgButton, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loadCNN_Sequential, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.exitButton, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.messageLayout = QHBoxLayout()
        self.messageLayout.addWidget(self.loadCNN_Sequential, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.messageLayout)

        layout.addLayout(self.messageLayout)
        self.imgButton.clicked.connect(self.create_dialog)
        self.loadCNN_Sequential.clicked.connect(self.loadCNN_Sequential_analysis)
        self.exitButton.clicked.connect(self.exit_app)


    def get_image(self, selectedFile):
        perceptron.image_path = selectedFile

    def run_perceptron(self):
        perceptron.run()

    def create_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp *.jpeg *.gif *.tif)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        file_dialog.fileSelected.connect(self.on_file_selected)
        file_dialog.exec()

    def on_file_selected(self, selected_file):
        self.selected_file = selected_file
        if self.selected_file:
            self.get_image(self.selected_file)

    def loadCNN_Sequential_analysis(self):
        if self.selected_file is not None:
            self.run_perceptron()
        else:
            self.loadCNN_Sequential.clicked.connect(self.analysis_warning)


    def analysis_warning(self):
        QMessageBox.warning(self, 'Warning',self.imageNotExist_warning)

    def exit_app(self):
        return self.close()
