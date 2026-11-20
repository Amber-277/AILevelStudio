
@tool
extends RefCounted


const GENERATED_NODE_NAME = "GeneratedLevel"
const GENERATED_META_KEY = "ai_level_studio_generated"
const BASE_CELL_SIZE: float = 64.0


# 将方向字符串转换为基础旋转角度
func get_direction_rotation(direction: Variant) -> float:

	match direction:
		"up":
			return 0.0

		"right":
			return 90.0

		"down":
			return 180.0

		"left":
			return 270.0

		_:
			return 0.0


# 创建地图，但暂时不加入当前场景
func generate_level(level_data: Dictionary) -> Node2D:

	var width: int = int(level_data["width"])
	var height: int = int(level_data["height"])

	# 将协议中的单元格大小映射为 Godot 像素
	var cell_size: float = BASE_CELL_SIZE * float(level_data["cell_size"])

	print("开始生成关卡：", level_data["name"])

	# 创建生成容器
	var generated = Node2D.new()
	generated.name = GENERATED_NODE_NAME
	generated.set_meta(GENERATED_META_KEY, true)

	# 生成背景
	var background = ColorRect.new()
	background.name = "Background"
	background.color = Color(0.12, 0.12, 0.16)
	background.position = Vector2.ZERO
	background.size = Vector2(
		width * cell_size,
		height * cell_size
	)

	generated.add_child(background)

	# 生成竖向网格线
	for x in range(width + 1):

		var line = Line2D.new()

		line.add_point(Vector2(x * cell_size, 0))
		line.add_point(Vector2(x * cell_size, height * cell_size))

		line.width = 1.0
		line.default_color = Color(0.35, 0.35, 0.4)

		generated.add_child(line)

	# 生成横向网格线
	for y in range(height + 1):

		var line = Line2D.new()

		line.add_point(Vector2(0, y * cell_size))
		line.add_point(Vector2(width * cell_size, y * cell_size))

		line.width = 1.0
		line.default_color = Color(0.35, 0.35, 0.4)

		generated.add_child(line)

	# 生成实体
	for entity in level_data["entities"]:

		var x: int = int(entity["position"]["x"])
		var y: int = int(entity["position"]["y"])

		# 左下角原点转换为 Godot 左上角原点
		var screen_y: int = height - 1 - y

		# 创建实体外层节点
		var entity_node = Node2D.new()
		entity_node.name = str(entity["id"])

		# 将实体放在对应网格的中心
		entity_node.position = Vector2(
			x * cell_size + cell_size * 0.5,
			screen_y * cell_size + cell_size * 0.5
		)

		# 计算最终旋转角度
		var direction_rotation: float = get_direction_rotation(
			entity.get("direction")
		)

		var extra_rotation: float = float(
			entity.get("rotation", 0.0)
		)

		entity_node.rotation_degrees = direction_rotation + extra_rotation

		# 根据实体类型生成不同外观
		if entity["type"] == "mirror":

			# 镜面外层：深青色
			var mirror_outline = Line2D.new()
			mirror_outline.name = "MirrorOutline"

			mirror_outline.add_point(
				Vector2(0, -cell_size * 0.32)
			)
			mirror_outline.add_point(
				Vector2(0, cell_size * 0.32)
			)

			mirror_outline.width = cell_size * 0.16
			mirror_outline.default_color = Color(0.02, 0.25, 0.35)

			entity_node.add_child(mirror_outline)

			# 镜面内层：明亮蓝色
			var mirror_surface = Line2D.new()
			mirror_surface.name = "MirrorSurface"

			mirror_surface.add_point(
				Vector2(0, -cell_size * 0.32)
			)
			mirror_surface.add_point(
				Vector2(0, cell_size * 0.32)
			)

			mirror_surface.width = cell_size * 0.09
			mirror_surface.default_color = Color(0.2, 0.85, 1.0)

			entity_node.add_child(mirror_surface)

		else:

			# 墙壁和其他实体仍然使用方块
			var block = ColorRect.new()
			block.name = "Visual"

			block.size = Vector2(
				cell_size * 0.8,
				cell_size * 0.8
			)

			block.position = Vector2(
				-cell_size * 0.4,
				-cell_size * 0.4
			)

			# 根据实体类型设置颜色
			if entity["type"] == "wall":
				block.color = Color(0.65, 0.65, 0.7)

			else:
				block.color = Color(1.0, 0.8, 0.2)

			entity_node.add_child(block)

		# 保存协议扩展信息，供以后使用
		entity_node.set_meta("entity_id", entity["id"])
		entity_node.set_meta("entity_type", entity["type"])
		entity_node.set_meta("entity_direction", entity.get("direction"))
		entity_node.set_meta("entity_layer", entity.get("layer", "default"))
		entity_node.set_meta("entity_asset_id", entity.get("asset_id"))
		entity_node.set_meta("entity_properties", entity.get("properties", {}))

		generated.add_child(entity_node)

	print("关卡生成完成！")

	return generated
