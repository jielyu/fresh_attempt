/***

   参考网页：https://blog.51cto.com/u_15127611/4201172
*/

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPainter>
#include <QMenuBar>
#include <QtSvg/QSvgGenerator>
#include <QFileDialog>


class MainWindow : public QMainWindow
{
    Q_OBJECT


public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();

    virtual void paintEvent(QPaintEvent *event);

public slots:
    void actionSaveAsSVG();

private:
    void paintAll(QSvgGenerator *generator = nullptr);
};

#endif // MAINWINDOW_H
