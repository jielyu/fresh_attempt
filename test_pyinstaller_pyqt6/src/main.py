import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

# 创建应用程序实例
app = QApplication(sys.argv)

# 创建主窗口
window = QWidget()
window.setWindowTitle("PyQt6 Hello World")
window.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

# 创建一个标签控件
label = QLabel("Hello, PyQt6 World!", parent=window)
label.move(100, 80)  # 在窗口中的位置

# 显示窗口
window.show()

# 运行应用程序主循环
sys.exit(app.exec())
