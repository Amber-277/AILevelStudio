
from pathlib import Path

from desktop.core.models.level import Level
from desktop.core.services.level_io import (
    load_level as load_level_from_file,
    save_level as save_level_to_file,
)
from desktop.core.validators.level_validator import (
    ValidationIssue,
    validate_level_rules,
)


class LevelController:
    """
    关卡控制器。

    负责协调：
    1. JSON 数据解析
    2. Schema 验证
    3. 关卡规则验证
    4. 关卡文件读取
    5. 关卡文件保存

    不负责界面显示，也不直接操作 Qt 控件。
    """

    # 解析 JSON 并验证数据结构
    def parse_level(self, json_text: str) -> Level:

        return Level.model_validate_json(json_text)

    # 验证关卡游戏规则
    def validate_level(
        self,
        level: Level
    ) -> list[ValidationIssue]:

        return validate_level_rules(level)

    # 读取关卡文件
    def open_level(self, file_path: str | Path) -> Level:

        return load_level_from_file(file_path)

    # 保存关卡文件
    def save_level(
        self,
        level: Level,
        file_path: str | Path
    ) -> None:

        # 保存前再次检查规则
        issues = self.validate_level(level)

        if issues:
            messages = "\n".join(
                f"[{issue.code}] {issue.message}"
                for issue in issues
            )

            raise ValueError(
                "关卡存在规则问题，无法保存：\n" + messages
            )

        save_level_to_file(level, file_path)

    # 同时执行结构验证和规则验证
    def validate_json(
        self,
        json_text: str
    ) -> tuple[Level, list[ValidationIssue]]:

        level = self.parse_level(json_text)

        issues = self.validate_level(level)

        return level, issues
