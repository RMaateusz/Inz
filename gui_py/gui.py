from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import perceptron
class Window (QWidget):
    descriptionImgButton = "Upload image"
    descriptionWindowTitle = "Image Recognition API made by Mateusz Rosa"
    descriptionWindowLocation_X = 50
    descriptionWindowLocation_Y = 50
    windowWidth = 250
    windowHeight = 250

    def __init__(self):
        super(Window, self).__init__()
        self.init_objects()
        self.update()
        self.show()

    def init_objects(self):
        self.layout = QVBoxLayout()
        self.imgButton = QPushButton(self.descriptionImgButton, self)

    def update(self):
        if Window:
            self.resize(self.windowWidth, self.windowHeight)

        if self.layout:
            self.layout.addWidget(self.imgButton, Qt.AlignmentFlag.AlignLeft)
            self.setLayout(self.layout)

        if self.imgButton:
            self.imgButton.move(0, 2*self.descriptionWindowLocation_Y)

    def button_clicked(self):
        self.imgButton.clicked.connect(self.create_dialog)

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

