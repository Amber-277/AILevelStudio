
import pytest

from desktop.core.models.level import Level
from desktop.core.validators.level_validator import (
    validate_level_rules,
)


def create_test_level(entities=None):
    """创建用于测试的基础关卡。"""

    return Level(
        level_id="test_level",
        name="验证器测试关卡",
        width=10,
        height=8,
        entities=entities or [],
    )


def create_entity(
    entity_id="entity_001",
    x=2,
    y=3,
    direction="up",
    rotation=0.0,
):
    """创建用于测试的实体。"""

    return {
        "id": entity_id,
        "type": "wall",
        "position": {
            "x": x,
            "y": y,
        },
        "direction": direction,
        "rotation": rotation,
    }


def test_valid_level_has_no_issues():
    """正常关卡不应该产生验证问题。"""

    level = create_test_level([
        create_entity(),
        create_entity(
            entity_id="entity_002",
            x=9,
            y=7,
            direction="left",
        ),
    ])

    issues = validate_level_rules(level)

    assert issues == []


def test_detect_duplicate_entity_id():
    """检测重复实体 ID。"""

    level = create_test_level([
        create_entity(entity_id="wall_001"),
        create_entity(entity_id="wall_001"),
    ])

    issues = validate_level_rules(level)

    assert any(
        issue.code == "DUPLICATE_ENTITY_ID"
        for issue in issues
    )


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (10, 3),
        (2, 8),
    ],
)
def test_detect_position_out_of_bounds(x, y):
    """检测超出地图范围的实体坐标。"""

    level = create_test_level([
        create_entity(x=x, y=y),
    ])

    issues = validate_level_rules(level)

    assert any(
        issue.code == "POSITION_OUT_OF_BOUNDS"
        for issue in issues
    )


@pytest.mark.parametrize(
    "direction",
    [
        "north",
        "diagonal",
        "invalid",
    ],
)
def test_detect_invalid_direction(direction):
    """检测不合法的实体方向。"""

    level = create_test_level([
        create_entity(direction=direction),
    ])

    issues = validate_level_rules(level)

    assert any(
        issue.code == "INVALID_DIRECTION"
        for issue in issues
    )


def test_accept_null_direction():
    """允许方向为空。"""

    level = create_test_level([
        create_entity(direction=None),
    ])

    issues = validate_level_rules(level)

    assert issues == []


def test_detect_non_finite_rotation():
    """检测 NaN 旋转角度。"""

    level = create_test_level([
        create_entity(rotation=float("nan")),
    ])

    issues = validate_level_rules(level)

    assert any(
        issue.code == "INVALID_ROTATION"
        for issue in issues
    )


def test_collect_multiple_issues():
    """一次收集同一个关卡中的多个问题。"""

    level = create_test_level([
        create_entity(
            entity_id="wall_001",
            x=10,
            direction="north",
        ),
        create_entity(
            entity_id="wall_001",
            y=8,
        ),
    ])

    issues = validate_level_rules(level)

    issue_codes = {
        issue.code
        for issue in issues
    }

    assert "DUPLICATE_ENTITY_ID" in issue_codes
    assert "POSITION_OUT_OF_BOUNDS" in issue_codes
    assert "INVALID_DIRECTION" in issue_codes
