#pragma once
#include "/VS_Projects/NeuralCPP/NeuralCPP/NeuralCNN.h"
#include <QtWidgets/QMainWindow>
#include "ui_CPPNeural.h"
#include <qlabel.h>
#include <qpushbutton.h>
#include <qlayout.h>
#include <string.h>

#ifndef GUI_H
#define GUI_H

class Window : public QWidget {
    Q_OBJECT

public:
    Window(QWidget* parent = nullptr);
                                                   
    void get_data(double data_loss, double data_acc);

private:
    double gui_acc;
    double gui_loss;

    int descriptionWindowLocation_X;
    int descriptionWindowLocation_Y;
    int windowWidth;
    int windowHeight;
    QString descriptionImgButton;
    QString descriptionExitButton;
    QString descriptionWindowTitle;
    QString descriptionLoadCNN_Sequential;
    QString imageNotExist_warning;

    QLabel* lossResult;
    QLabel* accuracyResult;
    QPushButton* imgButton;
    QPushButton* exitButton;
    QPushButton* loadCNN_Sequential;

    void initUI();
    void init_layout();

private slots:
    void create_dialog();
    void loadCNN_Sequential_analysis();
    void exit_app();
};

#endif // GUI_H