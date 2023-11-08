from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import perceptron
global gui_acc
global gui_loss
gui_acc = 0.0
gui_loss = 0.0

class Window (QWidget):
    def __init__(self):
        self.descriptionWindowLocation_X = 50
        self.descriptionWindowLocation_Y = 50
        self.windowWidth = 250
        self.windowHeight = 250
        self.descriptionImgButton = ""
        self.descriptionExitButton = ""
        self.descriptionWindowTitle = ""
        super(Window, self).__init__()
        self.setStyleSheet("background-color: darkgray;")  # Zmień na kolor tła, jaki chcesz

        self.initUI()
        self.show()
        self.selected_file = None
        self.isFinished = False

    def get_data(self, data_loss, data_acc):
        gui_acc= data_acc
        gui_loss = data_loss
        return gui_acc, gui_loss
    def initUI(self):
        self.descriptionImgButton = "Upload image"
        self.descriptionWindowTitle = "Image Recognition API made by Mateusz Rosa"
        self.descriptionExitButton = "Exit"
        self.descriptionLoadCNN_Sequential = "Sequential CNN Analysis"
        self.imageNotExist_warning = "Image is not uploaded!"

        self.setWindowTitle(self.descriptionWindowTitle)
        self.setGeometry(self.descriptionWindowLocation_X, self.descriptionWindowLocation_Y, self.windowWidth, self.windowHeight)

        self.lossResult = QLabel()
        self.accuracyResult = QLabel()
        self.imgButton = QPushButton(self.descriptionImgButton, self)
        self.exitButton = QPushButton(self.descriptionExitButton, self)
        self.loadCNN_Sequential = QPushButton(self.descriptionLoadCNN_Sequential, self)
        self.tensorboard_button = QPushButton("Generate chart")
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()

        self.init_layout()

        self.lossResult.setText(f"Loss rating: {gui_loss}")
        self.accuracyResult.setText(f"Accuracy rating: {gui_acc}")
        self.lossResult.setGeometry(0, 450, 100, 100)

        self.imgButton.clicked.connect(self.create_dialog)
        self.loadCNN_Sequential.clicked.connect(self.loadCNN_Sequential_analysis)
        self.exitButton.clicked.connect(self.exit_app)
        self.tensorboard_button.clicked.connect(self.open_tensorboard)

    def open_tensorboard(self):
        figure = perceptron.NeuralCNN.generate_plot()
        self.view.setScene(self.scene)
        self.canvas = FigureCanvas(figure)
        self.scene.addWidget(self.canvas)
        self.canvas.draw()

    def init_layout(self):
        self.layout = QVBoxLayout()
        self.messageLayout = QHBoxLayout()

        self.layout.addWidget(self.lossResult)
        self.layout.addWidget(self.accuracyResult)
        self.layout.addWidget(self.imgButton)
        self.layout.addWidget(self.view)
        self.messageLayout.addWidget(self.loadCNN_Sequential)
        self.layout.addWidget(self.loadCNN_Sequential)
        self.layout.addWidget(self.exitButton)
        self.layout.addWidget(self.tensorboard_button)

        self.setLayout(self.layout)
        self.setLayout(self.messageLayout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def updateData(self):
        self.lossResult.setText(f"Loss rating: {gui_loss}")
        self.accuracyResult.setText(f"Accuracy rating: {gui_acc}")

    def get_image(self, selectedFile):
        perceptron.image_path = selectedFile

    def run_perceptron(self):
        perceptron.run()
        self.updateData()

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
            self.analysis_warning()

    def analysis_warning(self):
        return QMessageBox.warning(self, 'Warning',self.imageNotExist_warning)

    def exit_app(self):
        return self.close()
