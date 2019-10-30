#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow){
    ui->setupUi(this);

    connected = false;

    tcpServer = new TcpServer();

    tcpServer->setIpAddress("127.0.0.1");
    tcpServer->setPort(5425);

    tcpServer->startServer();

    connect(tcpServer, SIGNAL(connectedClient()), this, SLOT(connectedClient()));

    connect(ui->btn1, SIGNAL(clicked()), this, SLOT(btn1Clicked()));
    connect(ui->btn2, SIGNAL(clicked()), this, SLOT(btn2Clicked()));
    connect(ui->btnQuit, SIGNAL(clicked()), this, SLOT(btnQuitClicked()));
}

MainWindow::~MainWindow(){
    delete ui;
}

void MainWindow::connectedClient(){
    connected = true;
    connect(tcpServer->socket[tcpServer->cnt], SIGNAL(readyRead()), this, SLOT(readMessage()), Qt::DirectConnection);
    connect(tcpServer->socket[tcpServer->cnt], SIGNAL(disconnected()), this, SLOT(disconnected()), Qt::DirectConnection);
    tcpServer->cnt++;
}

void MainWindow::readMessage(){
    QByteArray rxData;
    rxData = tcpServer->socket[0]->readAll();
    qDebug() << "rxData right : " << rxData;

    rxData = tcpServer->socket[1]->readAll();
    qDebug() << "rxData left : " << rxData;
}

void MainWindow::disconnected(){
    connected = false;
}

void MainWindow::btn1Clicked()
{
    txData.clear();
    txData.append(Qt::Key_S);
    txData.append(Qt::Key_M);
    txData.append(Qt::Key_A);
    txData.append(Qt::Key_S);
    txData.append(Qt::Key_E);
    tcpServer->socket[0]->write(txData);
    tcpServer->socket[1]->write(txData);

    qDebug() << "txData : " << txData;
}

void MainWindow::btn2Clicked()
{
    txData.clear();
    txData.append(Qt::Key_S);
    txData.append(Qt::Key_M);
    txData.append(Qt::Key_B);
    txData.append(Qt::Key_S);
    txData.append(Qt::Key_E);
    tcpServer->socket[0]->write(txData);
    tcpServer->socket[1]->write(txData);

    qDebug() << "txData : " << txData;
}

void MainWindow::btnQuitClicked()
{
    txData.clear();
    txData.append(Qt::Key_S);
    txData.append(Qt::Key_M);
    txData.append(Qt::Key_Q);
    txData.append(Qt::Key_S);
    txData.append(Qt::Key_E);
    tcpServer->socket[0]->write(txData);
    tcpServer->socket[1]->write(txData);

    qDebug() << "txData : " << txData;
}
