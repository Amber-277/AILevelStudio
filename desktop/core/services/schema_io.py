
import json
from pathlib import Path

from desktop.core.models.level import Level


def export_level_schema(file_path: str | Path) -> None:
    """
    根据 Level 模型生成 JSON Schema 文件。
    """

    path = Path(file_path)

    # 自动创建目标目录
    path.parent.mkdir(parents=True, exist_ok=True)

    # 从 Pydantic 模型生成 JSON Schema
    schema = Level.model_json_schema()

    # 明确指定 JSON Schema 标准版本
    schema["$schema"] = (
        "https://json-schema.org/draft/2020-12/schema"
    )

    # 写入文件
    json_data = json.dumps(
        schema,
        ensure_ascii=False,
        indent=4
    )

    path.write_text(json_data, encoding="utf-8")

    print(f"JSON Schema 已生成：{path.resolve()}")
