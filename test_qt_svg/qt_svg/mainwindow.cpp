#include "mainwindow.h"
#include <QAction>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    QMenu *fileMenu = menuBar()->addMenu(QObject::tr("&File"));
    QAction * qaction = new QAction(QObject::tr("Save As Svg"), this);
    connect(qaction, SIGNAL(triggered()), this,  SLOT(actionSaveAsSVG()));
    fileMenu->addAction(qaction);
}

MainWindow::~MainWindow()
{

}

void MainWindow::paintEvent(QPaintEvent *event)
{
    paintAll();
}

void MainWindow::actionSaveAsSVG()
{

    qDebug("enter actionSaveAsSVG");
    QString filePath = QFileDialog::getSaveFileName(this, "Save SVG",

                                                    "", "SVG files (*.svg)");
    if (filePath == "")
        return;
    QSvgGenerator generator;
    generator.setFileName(filePath);
    generator.setSize(QSize(this->width(), this->height()));
    generator.setViewBox(QRect(0, 0, this->width(), this->height()));
    generator.setTitle("SVG Example");
    generator.setDescription("This SVG file is generated by Qt.");
    paintAll(&generator);
}

void MainWindow::paintAll(QSvgGenerator *generator)
{
    QPainter painter;
    if (generator)
        painter.begin(generator);
    else
        painter.begin(this);

    // Draw Text
    painter.setFont(QFont("Times", 14, QFont::Bold));
    painter.drawText(QPoint(20, 40), "Hello Qt");
    // Draw Line
    painter.drawLine(QPoint(50, 70), QPoint(100, 100));
    // Draw Rectangle
    // 这里绘制的是位图
    painter.setBrush(Qt::BDiagPattern);
    painter.drawRect(QRect(40, 120, 80, 30));
    // Draw Ellipse
    // 这里绘制的是位图
    QPen ellipsePen;
    ellipsePen.setColor(Qt::red);
    ellipsePen.setStyle(Qt::DashDotLine);
    painter.setPen(ellipsePen);
    painter.drawEllipse(QPoint(80, 200), 50, 20);
    // Draw Rectangle
    // 这里绘制的是矢量图
    QPainterPath rectPath;
    rectPath.addRect(QRect(150, 30, 100, 50));
    painter.setPen(QPen(Qt::red, 1, Qt::DashDotLine, Qt::FlatCap,
                        Qt::MiterJoin));
    painter.setBrush(Qt::yellow);
    painter.drawPath(rectPath);
    // Draw Ellipse
    QPainterPath ellipsePath;
    ellipsePath.addEllipse(QPoint(200, 120), 50, 20);
    painter.setPen(QPen(QColor(79, 106, 25), 5, Qt::SolidLine,
                        Qt::FlatCap, Qt::MiterJoin));
    painter.setBrush(QColor(122, 163, 39));
    painter.drawPath(ellipsePath);
    painter.end();
}
