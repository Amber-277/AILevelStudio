
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication


# 将项目根目录加入 Python 模块搜索路径
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))


from desktop.app.main_window import MainWindow


def main():

	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
