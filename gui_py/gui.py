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

    def initUI(self):
        self.descriptionImgButton = "Upload image"
        self.descriptionWindowTitle = "Image Recognition API made by Mateusz Rosa"
        self.descriptionExitButton = "Exit"
        self.descriptionWindowLocation_X = 50
        self.descriptionWindowLocation_Y = 50
        self.windowWidth = 250
        self.windowHeight = 250

        self.setWindowTitle(self.descriptionWindowTitle)
        self.setGeometry(self.descriptionWindowLocation_X, self.descriptionWindowLocation_Y, self.windowWidth, self.windowHeight)

        layout = QVBoxLayout()

        imgButton = QPushButton(self.descriptionImgButton, self)
        exitButton = QPushButton(self.descriptionExitButton, self)

        layout.addWidget(imgButton, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exitButton, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        imgButton.clicked.connect(self.create_dialog)
        exitButton.clicked.connect(self.exit_app)

    def get_image(self, selectedFile):
        perceptron.image_path = selectedFile
        self.run_perceptron()

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
        if selected_file:
            self.get_image(selected_file)

    def exit_app(self):
        return self.close()
