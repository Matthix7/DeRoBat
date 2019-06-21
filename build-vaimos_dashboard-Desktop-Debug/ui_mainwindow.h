/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.5.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>
#include "widgetVaimos.h"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    widgetVaimos *widgetVaimos1;
    QScrollBar *k0_horizontalScrollBar;
    QScrollBar *Echelle_verticalScrollBar;
    QPushButton *pushButtonLoadFile;
    QScrollBar *Step_verticalScrollBar;
    QCheckBox *Wind_checkBox;
    QCheckBox *Sail1_checkBox;
    QCheckBox *Sail2_checkBox;
    QCheckBox *Text_checkBox;
    QCheckBox *Go_checkBox;
    QScrollBar *ks0_verticalScrollBar;
    QScrollBar *ks1_verticalScrollBar;
    QLabel *ks0_label;
    QLabel *ks1_label;
    QLabel *Echelle_label;
    QLabel *Step_label;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->setEnabled(true);
        MainWindow->resize(1000, 650);
        MainWindow->setMinimumSize(QSize(1000, 650));
        MainWindow->setMaximumSize(QSize(1000, 650));
        MainWindow->setCursor(QCursor(Qt::PointingHandCursor));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        widgetVaimos1 = new widgetVaimos(centralWidget);
        widgetVaimos1->setObjectName(QStringLiteral("widgetVaimos1"));
        widgetVaimos1->setGeometry(QRect(120, 30, 600, 600));
        widgetVaimos1->setMinimumSize(QSize(600, 600));
        k0_horizontalScrollBar = new QScrollBar(centralWidget);
        k0_horizontalScrollBar->setObjectName(QStringLiteral("k0_horizontalScrollBar"));
        k0_horizontalScrollBar->setGeometry(QRect(20, 0, 701, 20));
        k0_horizontalScrollBar->setMinimum(0);
        k0_horizontalScrollBar->setMaximum(50000);
        k0_horizontalScrollBar->setSingleStep(1);
        k0_horizontalScrollBar->setValue(0);
        k0_horizontalScrollBar->setOrientation(Qt::Horizontal);
        Echelle_verticalScrollBar = new QScrollBar(centralWidget);
        Echelle_verticalScrollBar->setObjectName(QStringLiteral("Echelle_verticalScrollBar"));
        Echelle_verticalScrollBar->setGeometry(QRect(20, 60, 21, 311));
        Echelle_verticalScrollBar->setMinimum(1);
        Echelle_verticalScrollBar->setMaximum(100);
        Echelle_verticalScrollBar->setSingleStep(1);
        Echelle_verticalScrollBar->setValue(25);
        Echelle_verticalScrollBar->setOrientation(Qt::Vertical);
        pushButtonLoadFile = new QPushButton(centralWidget);
        pushButtonLoadFile->setObjectName(QStringLiteral("pushButtonLoadFile"));
        pushButtonLoadFile->setGeometry(QRect(760, 0, 75, 23));
        Step_verticalScrollBar = new QScrollBar(centralWidget);
        Step_verticalScrollBar->setObjectName(QStringLiteral("Step_verticalScrollBar"));
        Step_verticalScrollBar->setGeometry(QRect(70, 60, 16, 311));
        Step_verticalScrollBar->setMinimum(1);
        Step_verticalScrollBar->setValue(10);
        Step_verticalScrollBar->setOrientation(Qt::Vertical);
        Wind_checkBox = new QCheckBox(centralWidget);
        Wind_checkBox->setObjectName(QStringLiteral("Wind_checkBox"));
        Wind_checkBox->setGeometry(QRect(760, 70, 70, 17));
        Wind_checkBox->setChecked(true);
        Sail1_checkBox = new QCheckBox(centralWidget);
        Sail1_checkBox->setObjectName(QStringLiteral("Sail1_checkBox"));
        Sail1_checkBox->setEnabled(true);
        Sail1_checkBox->setGeometry(QRect(760, 100, 151, 17));
        Sail1_checkBox->setAcceptDrops(false);
        Sail1_checkBox->setChecked(false);
        Sail2_checkBox = new QCheckBox(centralWidget);
        Sail2_checkBox->setObjectName(QStringLiteral("Sail2_checkBox"));
        Sail2_checkBox->setGeometry(QRect(760, 130, 101, 17));
        Sail2_checkBox->setChecked(true);
        Text_checkBox = new QCheckBox(centralWidget);
        Text_checkBox->setObjectName(QStringLiteral("Text_checkBox"));
        Text_checkBox->setGeometry(QRect(760, 40, 70, 17));
        Text_checkBox->setChecked(true);
        Go_checkBox = new QCheckBox(centralWidget);
        Go_checkBox->setObjectName(QStringLiteral("Go_checkBox"));
        Go_checkBox->setGeometry(QRect(760, 160, 81, 17));
        Go_checkBox->setChecked(true);
        ks0_verticalScrollBar = new QScrollBar(centralWidget);
        ks0_verticalScrollBar->setObjectName(QStringLiteral("ks0_verticalScrollBar"));
        ks0_verticalScrollBar->setGeometry(QRect(760, 240, 16, 331));
        ks0_verticalScrollBar->setOrientation(Qt::Vertical);
        ks1_verticalScrollBar = new QScrollBar(centralWidget);
        ks1_verticalScrollBar->setObjectName(QStringLiteral("ks1_verticalScrollBar"));
        ks1_verticalScrollBar->setGeometry(QRect(810, 240, 16, 331));
        ks1_verticalScrollBar->setOrientation(Qt::Vertical);
        ks0_label = new QLabel(centralWidget);
        ks0_label->setObjectName(QStringLiteral("ks0_label"));
        ks0_label->setGeometry(QRect(760, 220, 46, 13));
        ks1_label = new QLabel(centralWidget);
        ks1_label->setObjectName(QStringLiteral("ks1_label"));
        ks1_label->setGeometry(QRect(810, 220, 46, 13));
        Echelle_label = new QLabel(centralWidget);
        Echelle_label->setObjectName(QStringLiteral("Echelle_label"));
        Echelle_label->setGeometry(QRect(20, 40, 46, 13));
        Step_label = new QLabel(centralWidget);
        Step_label->setObjectName(QStringLiteral("Step_label"));
        Step_label->setGeometry(QRect(70, 40, 46, 13));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1000, 20));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Interface pour VAIMOS (luc.jaulin@ensta-bretagne.fr)", 0));
        pushButtonLoadFile->setText(QApplication::translate("MainWindow", "Load file", 0));
        Wind_checkBox->setText(QApplication::translate("MainWindow", "Wind", 0));
        Sail1_checkBox->setText(QApplication::translate("MainWindow", "Sail with compass", 0));
        Sail2_checkBox->setText(QApplication::translate("MainWindow", "Sail with motor", 0));
        Text_checkBox->setText(QApplication::translate("MainWindow", "Text", 0));
        Go_checkBox->setText(QApplication::translate("MainWindow", "Go direction", 0));
        ks0_label->setText(QApplication::translate("MainWindow", "ks0", 0));
        ks1_label->setText(QApplication::translate("MainWindow", "ks1", 0));
        Echelle_label->setText(QApplication::translate("MainWindow", "Echelle", 0));
        Step_label->setText(QApplication::translate("MainWindow", "Step", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
