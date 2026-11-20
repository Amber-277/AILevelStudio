@tool
extends Node2D


func _ready() -> void:
	pass


# 接收插件传入的关卡数据
func load_level(level_data: Dictionary) -> void:
	generate_level(level_data)


# 根据关卡数据生成地图
func generate_level(level_data: Dictionary) -> void:
	# 清理上一次生成的地图
	for child in get_children():
		child.queue_free()

	# 读取地图信息
	var width = int(level_data["width"])
	var height = int(level_data["height"])
	var cell_size = 64

	print("开始生成关卡：", level_data["name"])

	# 生成地图背景
	var background = ColorRect.new()
	background.color = Color(0.12, 0.12, 0.16)
	background.position = Vector2.ZERO
	background.size = Vector2(width * cell_size, height * cell_size)
	add_child(background)

	# 生成竖向网格线
	for x in range(width + 1):
		var line = Line2D.new()
		line.add_point(Vector2(x * cell_size, 0))
		line.add_point(Vector2(x * cell_size, height * cell_size))
		line.width = 1.0
		line.default_color = Color(0.35, 0.35, 0.4)
		add_child(line)

	# 生成横向网格线
	for y in range(height + 1):
		var line = Line2D.new()
		line.add_point(Vector2(0, y * cell_size))
		line.add_point(Vector2(width * cell_size, y * cell_size))
		line.width = 1.0
		line.default_color = Color(0.35, 0.35, 0.4)
		add_child(line)

	# 生成关卡实体
	for entity in level_data["entities"]:
		var x = int(entity["position"]["x"])
		var y = int(entity["position"]["y"])

		# 转换左下角原点为 Godot 左上角原点
		var screen_y = height - 1 - y

		var block = ColorRect.new()
		block.size = Vector2(cell_size * 0.8, cell_size * 0.8)
		block.position = Vector2(
			x * cell_size + cell_size * 0.1,
			screen_y * cell_size + cell_size * 0.1
		)

		if entity["type"] == "wall":
			block.color = Color(0.65, 0.65, 0.7)
		elif entity["type"] == "mirror":
			block.color = Color(0.2, 0.8, 1.0)
		else:
			block.color = Color(1.0, 0.8, 0.2)

		add_child(block)

	print("关卡生成完成！")
