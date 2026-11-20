
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from desktop.app.controllers.level_controller import LevelController


PROJECT_ROOT = Path(__file__).resolve().parents[2]


SAMPLE_LEVEL = {
    "protocol_version": "1.0",
    "level_id": "my_first_level",
    "name": "我的第一个关卡",
    "description": "桌面程序生成的测试关卡",
    "width": 10,
    "height": 8,
    "cell_size": 1.0,
    "coordinate_system": "cartesian_y_up",
    "entities": []
}


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_file_path = None
        self.controller = LevelController()

        self.setWindowTitle("AI Level Studio")
        self.resize(1100, 700)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # 标题
        title = QLabel("AI Level Studio")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold; padding: 8px;"
        )

        subtitle = QLabel(
            "AI-powered Level Design Workbench"
        )
        subtitle.setStyleSheet(
            "font-size: 13px; color: gray; padding-left: 10px;"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # 顶部工具栏
        file_layout = QHBoxLayout()

        self.new_button = QPushButton("新建关卡")
        self.new_button.clicked.connect(self.new_level)

        file_layout.addWidget(self.new_button)
        file_layout.addStretch()

        main_layout.addLayout(file_layout)

        # 左右分栏
        splitter = QSplitter()

        # 左侧：需求输入
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        request_title = QLabel("关卡需求")
        request_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.request_editor = QTextEdit()
        self.request_editor.setPlaceholderText(
            "在这里描述你想制作的关卡……\n\n"
            "例如：\n"
            "制作一个 10×8 的解谜关卡，"
            "包含墙壁和镜子。"
        )

        self.generate_button = QPushButton(
            "AI 生成关卡（尚未接入）"
        )
        self.generate_button.setEnabled(False)

        left_layout.addWidget(request_title)
        left_layout.addWidget(self.request_editor)
        left_layout.addWidget(self.generate_button)

        # 右侧：JSON 编辑
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        json_header_layout = QHBoxLayout()

        json_title = QLabel("关卡 JSON")
        json_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.open_button = QPushButton("打开 JSON")
        self.open_button.clicked.connect(self.open_json)

        json_header_layout.addWidget(json_title)
        json_header_layout.addStretch()
        json_header_layout.addWidget(self.open_button)

        self.json_editor = QTextEdit()
        self.json_editor.setStyleSheet(
            "font-family: Consolas, monospace;"
            "font-size: 13px;"
        )

        self.json_editor.setPlainText(
            json.dumps(
                SAMPLE_LEVEL,
                ensure_ascii=False,
                indent=4
            )
        )
        self.json_editor.document().setModified(False)

        right_layout.addLayout(json_header_layout)
        right_layout.addWidget(self.json_editor)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 650])

        main_layout.addWidget(splitter)

        # 底部操作栏
        action_layout = QHBoxLayout()

        self.validate_button = QPushButton("验证 JSON")
        self.save_button = QPushButton("保存 JSON")

        self.validate_button.clicked.connect(
            self.validate_json
        )
        self.save_button.clicked.connect(
            self.save_json
        )

        action_layout.addWidget(self.validate_button)
        action_layout.addWidget(self.save_button)

        main_layout.addLayout(action_layout)

        # 状态栏
        self.status_label = QLabel(
            "就绪。请新建关卡或打开已有 JSON。"
        )
        self.status_label.setStyleSheet(
            "padding: 8px;"
        )

        main_layout.addWidget(self.status_label)

        self.setCentralWidget(central_widget)

     # 设置状态栏
    def set_status(self, message: str, color: str = "black"):

        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            f"padding: 8px; color: {color};"
        )

    # 格式化规则验证问题
    def format_rule_issues(self, issues) -> str:

        return "\n".join(
            f"[{issue.code}] {issue.message}"
            for issue in issues
        )

    # 检查是否存在未保存的修改
    def confirm_discard_changes(self) -> bool:

        has_unsaved_changes = (
            self.json_editor.document().isModified()
            or bool(self.request_editor.toPlainText().strip())
        )

        if not has_unsaved_changes:
            return True

        result = QMessageBox.question(
            self,
            "未保存的修改",
            "当前内容可能尚未保存。\n确定要放弃当前修改吗？",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        return result == QMessageBox.StandardButton.Yes

    # 新建关卡
    def new_level(self):

        if not self.confirm_discard_changes():
            return

        self.current_file_path = None
        self.request_editor.clear()

        self.json_editor.setPlainText(
            json.dumps(
                SAMPLE_LEVEL,
                ensure_ascii=False,
                indent=4
            )
        )

        self.json_editor.document().setModified(False)

        self.setWindowTitle("AI Level Studio - 未命名关卡")
        self.set_status("已创建新关卡。")

    # 打开 JSON 文件
    def open_json(self):

        if not self.confirm_discard_changes():
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "打开关卡 JSON",
            str(PROJECT_ROOT / "protocol"),
            "JSON 文件 (*.json)"
        )

        if not file_path:
            return

        try:
            level = self.controller.open_level(file_path)

            formatted_json = level.model_dump_json(
                indent=4,
                exclude_none=True
            )

            self.json_editor.setPlainText(formatted_json)
            self.json_editor.document().setModified(False)

            self.request_editor.clear()

            self.current_file_path = Path(file_path)

            self.setWindowTitle(
                f"AI Level Studio - {self.current_file_path.name}"
            )

            self.set_status(
                f"打开成功：{self.current_file_path}",
                "green"
            )

        except Exception as error:

            QMessageBox.warning(
                self,
                "打开失败",
                str(error)
            )

    # 验证 JSON
    def validate_json(self):

        json_text = self.json_editor.toPlainText()

        try:
            level, issues = self.controller.validate_json(json_text)

            if issues:

                messages = self.format_rule_issues(issues)

                self.set_status(
                    f"发现 {len(issues)} 个关卡规则问题。",
                    "red"
                )

                QMessageBox.warning(
                    self,
                    "关卡规则验证失败",
                    messages
                )
                return

            self.set_status(
                f"验证成功：{level.name} "
                f"({level.width} × {level.height})",
                "green"
            )

        except Exception as error:

            self.set_status(
                "JSON 验证失败，请检查数据。",
                "red"
            )

            QMessageBox.warning(
                self,
                "关卡验证失败",
                str(error)
            )

    # 保存 JSON
    def save_json(self):

        json_text = self.json_editor.toPlainText()

        # 先解析 JSON 和验证 Schema
        try:
            level = self.controller.parse_level(json_text)

        except Exception as error:

            QMessageBox.warning(
                self,
                "无法保存",
                "关卡数据结构验证失败：\n\n" + str(error)
            )
            return

        # 如果尚无文件路径，弹出另存为窗口
        if self.current_file_path is None:

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存关卡 JSON",
                str(
                    PROJECT_ROOT
                    / "protocol"
                    / (level.level_id + ".json")
                ),
                "JSON 文件 (*.json)"
            )

            if not file_path:
                return

            target_path = Path(file_path)

        else:
            target_path = self.current_file_path

        try:
            # 控制器负责规则验证和实际保存
            self.controller.save_level(level, target_path)

            self.current_file_path = target_path

            self.json_editor.document().setModified(False)

            self.setWindowTitle(
                f"AI Level Studio - {self.current_file_path.name}"
            )

            self.set_status(
                f"保存成功：{self.current_file_path}",
                "green"
            )

        except (ValueError, OSError) as error:

            QMessageBox.warning(
                self,
                "保存失败",
                str(error)
            )
