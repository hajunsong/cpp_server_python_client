#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include "tcpserver.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    // socket event
    void connectedClient();
    void readMessage();
    void disconnected();

    // button event
    void btn1Clicked();
    void btn2Clicked();
    void btnQuitClicked();

private:
    Ui::MainWindow *ui;
    TcpServer *tcpServer;
    bool connected;
    QByteArray txData;
};

#endif // MAINWINDOW_H
