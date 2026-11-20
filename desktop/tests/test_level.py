from desktop.core.services.schema_io import export_level_schema
from desktop.core.services.level_io import save_level, load_level
import pytest
from pydantic import ValidationError

from desktop.core.models.level import Level


def test_create_valid_level():
    """测试能否成功创建一个合法关卡。"""

    data = {
        "level_id": "level_001",
        "name": "First Laser Puzzle",
        "width": 10,
        "height": 8,
        "entities": [
            {
                "id": "laser_01",
                "type": "laser",
                "position": {
                    "x": 0,
                    "y": 3
                },
                "direction": "right"
            },
            {
                "id": "mirror_01",
                "type": "mirror",
                "position": {
                    "x": 4,
                    "y": 3
                }
            },
            {
                "id": "target_01",
                "type": "target",
                "position": {
                    "x": 8,
                    "y": 3
                }
            }
        ]
    }

    level = Level.model_validate(data)

    assert level.level_id == "level_001"
    assert level.width == 10
    assert len(level.entities) == 3


def test_reject_negative_coordinates():
    """测试是否拒绝负数坐标。"""

    data = {
        "level_id": "level_002",
        "name": "Invalid Level",
        "width": 10,
        "height": 8,
        "entities": [
            {
                "id": "laser_01",
                "type": "laser",
                "position": {
                    "x": -1,
                    "y": 3
                },
                "direction": "right"
            }
        ]
    }

    with pytest.raises(ValidationError):
        Level.model_validate(data)



def test_accept_custom_entity_type():
    """通用协议应该允许扩展实体类型。"""

    data = {
        "level_id": "level_003",
        "name": "Custom Entity Test",
        "width": 10,
        "height": 8,
        "entities": [
            {
                "id": "portal_01",
                "type": "teleporter",
                "position": {
                    "x": 2,
                    "y": 2
                },
                "properties": {
                    "target_id": "portal_02"
                }
            }
        ]
    }

    level = Level.model_validate(data)

    assert level.entities[0].type == "teleporter"
    assert level.entities[0].properties["target_id"] == "portal_02"
        
def test_save_and_load_level(tmp_path):
    """测试关卡能否保存并重新读取。"""

    data = {
        "level_id": "level_004",
        "name": "激光反射测试关卡",
        "width": 10,
        "height": 8,
        "entities": [
            {
                "id": "laser_01",
                "type": "laser",
                "position": {"x": 0, "y": 3},
                "direction": "right"
            },
            {
                "id": "target_01",
                "type": "target",
                "position": {"x": 8, "y": 3}
            }
        ]
    }

    original_level = Level.model_validate(data)

    file_path = tmp_path / "level.json"

    save_level(original_level, file_path)

    loaded_level = load_level(file_path)

    assert loaded_level.level_id == original_level.level_id
    assert loaded_level.name == original_level.name
    assert len(loaded_level.entities) == 2


def test_load_missing_file():
    """测试读取不存在的文件时是否正确报错。"""

    from desktop.core.services.level_io import load_level

    with pytest.raises(FileNotFoundError):
        load_level("this_file_does_not_exist.json")
        
def test_export_level_schema(tmp_path):
    """测试能否正确生成 JSON Schema。"""

    import json

    schema_path = tmp_path / "level_v1.schema.json"

    export_level_schema(schema_path)

    assert schema_path.exists()

    schema = json.loads(
        schema_path.read_text(encoding="utf-8")
    )

    assert schema["$schema"] == (
        "https://json-schema.org/draft/2020-12/schema"
    )

    assert "properties" in schema

    assert "entities" in schema["properties"]
    assert "width" in schema["properties"]
    assert "height" in schema["properties"]
