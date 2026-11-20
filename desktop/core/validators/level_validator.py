
import math
from dataclasses import dataclass

from desktop.core.models.level import Level


VALID_DIRECTIONS = {
    "up",
    "down",
    "left",
    "right",
}


@dataclass(frozen=True)
class ValidationIssue:
    """一条结构化的关卡验证问题。"""

    code: str
    message: str
    entity_id: str | None = None


def validate_level_rules(level: Level) -> list[ValidationIssue]:
    """
    检查关卡数据的游戏规则。

    注意：
    这里不负责 JSON 格式验证。
    JSON 和字段类型验证已经由 Pydantic Level 模型负责。
    """

    issues: list[ValidationIssue] = []

    # 记录已经出现过的实体 ID
    seen_ids: set[str] = set()

    # 遍历所有实体
    for index, entity in enumerate(level.entities):

        entity_id = entity.id

        # 1. 检查实体 ID 是否重复
        if entity_id in seen_ids:

            issues.append(
                ValidationIssue(
                    code="DUPLICATE_ENTITY_ID",
                    message=(
                        f"第 {index + 1} 个实体的 ID "
                        f"'{entity_id}' 重复。"
                    ),
                    entity_id=entity_id,
                )
            )

        else:
            seen_ids.add(entity_id)

        # 2. 检查 X 坐标是否越界
        x = entity.position.x

        if not 0 <= x < level.width:

            issues.append(
                ValidationIssue(
                    code="POSITION_OUT_OF_BOUNDS",
                    message=(
                        f"实体 '{entity_id}' 的 X 坐标为 {x}，"
                        f"超出有效范围 0 到 {level.width - 1}。"
                    ),
                    entity_id=entity_id,
                )
            )

        # 3. 检查 Y 坐标是否越界
        y = entity.position.y

        if not 0 <= y < level.height:

            issues.append(
                ValidationIssue(
                    code="POSITION_OUT_OF_BOUNDS",
                    message=(
                        f"实体 '{entity_id}' 的 Y 坐标为 {y}，"
                        f"超出有效范围 0 到 {level.height - 1}。"
                    ),
                    entity_id=entity_id,
                )
            )

        # 4. 检查 direction 是否合法
        direction = entity.direction

        if (
            direction is not None
            and direction not in VALID_DIRECTIONS
        ):

            issues.append(
                ValidationIssue(
                    code="INVALID_DIRECTION",
                    message=(
                        f"实体 '{entity_id}' 的方向 "
                        f"'{direction}' 不合法。"
                        "允许的方向为 up、down、left、right 或 null。"
                    ),
                    entity_id=entity_id,
                )
            )

        # 5. 检查 rotation 是否为有限数值
        if not math.isfinite(entity.rotation):

            issues.append(
                ValidationIssue(
                    code="INVALID_ROTATION",
                    message=(
                        f"实体 '{entity_id}' 的旋转角度 "
                        "必须是有限数值。"
                    ),
                    entity_id=entity_id,
                )
            )

    return issues
