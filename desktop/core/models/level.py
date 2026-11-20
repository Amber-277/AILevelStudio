
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# 1. 坐标模型
# ==========================================

class Position(BaseModel):
    """二维网格坐标，左下角为原点。"""

    model_config = ConfigDict(extra="forbid")

    x: int = Field(ge=0, description="横向网格坐标")
    y: int = Field(ge=0, description="纵向网格坐标")


# ==========================================
# 2. 关卡实体模型
# ==========================================


class LevelEntity(BaseModel):
    """关卡中的一个实体。"""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        min_length=1,
        description="实体唯一 ID"
    )

    type: str = Field(
        min_length=1,
        description="实体类型，例如 laser、mirror、wall"
    )

    position: Position

    direction: str | None = Field(
        default=None,
        description="实体朝向，例如 up、down、left、right"
    )

    rotation: float = Field(
        default=0.0,
        description="旋转角度，单位为度，正数表示逆时针"
    )

    layer: str = Field(
        default="default",
        min_length=1,
        description="实体所属图层"
    )

    asset_id: str | None = Field(
        default=None,
        description="资源标识，由引擎适配器映射"
    )

    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="实体自定义属性"
    )



# ==========================================
# 3. 关卡模型
# ==========================================

class Level(BaseModel):
    """AI Level Studio 通用 2D 关卡协议。"""

    model_config = ConfigDict(extra="forbid")

    protocol_version: Literal["1.0"] = "1.0"

    level_id: str = Field(min_length=1)

    name: str = Field(min_length=1)

    description: str = ""

    width: int = Field(ge=1, le=1000)

    height: int = Field(ge=1, le=1000)

    cell_size: float = Field(
        default=1.0,
        gt=0,
        description="每个网格单元的逻辑尺寸"
    )

    coordinate_system: Literal["cartesian_y_up"] = "cartesian_y_up"

    entities: list[LevelEntity] = Field(
        default_factory=list,
        description="关卡实体列表"
    )
