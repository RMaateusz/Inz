#include "NeuralGUI.h"

Window::Window(QWidget* parent) : QWidget(parent) {
    // Inicjalizacja zmiennych i ustawienia GUI
    short descriptionWindowLocation_X = 50;
    short descriptionWindowLocation_Y = 50;
    short windowWidth = 250;
    short windowHeight = 250;
    std::string descriptionImgButton = "Upload image";
    std::string descriptionExitButton = "Exit";
    std::string descriptionWindowTitle = "Image Recognition API made by Mateusz Rosa";
    std::string descriptionLoadCNN_Sequential = "Sequential CNN Analysis";
    std::string imageNotExist_warning = "Image is not uploaded!";
    float gui_loss = 0.0;

    setStyleSheet("background-color: darkgray;");  // Zmieñ na kolor t³a, jaki chcesz

    initUI();
    show();
}

void Window::get_data(double data_loss, double data_acc) {
    gui_acc = data_acc;
    gui_loss = data_loss;
}

void Window::initUI() {
    setWindowTitle(descriptionWindowTitle);
    setGeometry(descriptionWindowLocation_X, descriptionWindowLocation_Y, windowWidth, windowHeight);

    lossResult = new QLabel(this);
    accuracyResult = new QLabel(this);
    imgButton = new QPushButton(descriptionImgButton, this);
    exitButton = new QPushButton(descriptionExitButton, this);
    loadCNN_Sequential = new QPushButton(descriptionLoadCNN_Sequential, this);

    lossResult->setText("Loss rating: " + QString::number(gui_loss));
    accuracyResult->setText("Accuracy rating: " + QString::number(gui_acc));
    lossResult->setGeometry(0, 450, 100, 100);

    connect(imgButton, SIGNAL(clicked()), this, SLOT(create_dialog()));
    connect(loadCNN_Sequential, SIGNAL(clicked()), this, SLOT(loadCNN_Sequential_analysis()));
    connect(exitButton, SIGNAL(clicked()), this, SLOT(exit_app()));

    init_layout();
}

void Window::init_layout() {
    QVBoxLayout* layout = new QVBoxLayout(this);
    QHBoxLayout* messageLayout = new QHBoxLayout(this);

    layout->addWidget(lossResult);
    layout->addWidget(accuracyResult);
    layout->addWidget(imgButton);
    messageLayout->addWidget(loadCNN_Sequential);
    layout->addWidget(loadCNN_Sequential);
    layout->addWidget(exitButton);

    setLayout(layout);
    setLayout(messageLayout);
}

void Window::create_dialog() {
    // Dodaj obs³ugê wybierania obrazu
}

void Window::loadCNN_Sequential_analysis() {
    // Dodaj obs³ugê analizy obrazu z wykorzystaniem CNN
}

void Window::exit_app() {
    qApp->exit();
}
