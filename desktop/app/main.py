
print("===== AI Level Studio 启动测试 =====")

import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


print("PySide6 导入成功！")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("正在创建窗口……")

        self.setWindowTitle("AI Level Studio")
        self.resize(900, 600)

        label = QLabel("AI Level Studio is running!")
        label.setStyleSheet("""
            font-size: 24px;
            padding: 20px;
        """)

        self.setCentralWidget(label)


if __name__ == "__main__":
    print("正在启动 Qt……")

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    print("窗口已创建，等待事件循环……")

    sys.exit(app.exec())
