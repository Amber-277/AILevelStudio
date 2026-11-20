
import json
from pathlib import Path

from desktop.core.models.level import Level


def save_level(level: Level, file_path: str | Path) -> None:
    """
    将 Level 对象保存为 JSON 文件。
    """

    path = Path(file_path)

    # 确保目标文件夹存在
    path.parent.mkdir(parents=True, exist_ok=True)

    # 转换为 JSON 数据
    json_data = level.model_dump_json(
        indent=4,
        exclude_none=True
    )

    # 写入文件
    path.write_text(json_data, encoding="utf-8")


def load_level(file_path: str | Path) -> Level:
    """
    从 JSON 文件读取关卡，并验证数据是否合法。
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"关卡文件不存在：{path}")

    json_data = path.read_text(encoding="utf-8")

    # 解析 JSON 并通过 Pydantic 验证
    return Level.model_validate_json(json_data)
