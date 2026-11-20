
@tool
extends RefCounted


# 判断一个数值是否为有限数字
func is_finite_number(value: Variant) -> bool:
	if typeof(value) != TYPE_INT and typeof(value) != TYPE_FLOAT:
		return false

	return is_finite(float(value))


# 判断一个数字是否为整数值
func is_integer_number(value: Variant) -> bool:
	if not is_finite_number(value):
		return false

	return floor(float(value)) == float(value)


# 验证关卡数据
func validate_level_data(data: Dictionary) -> bool:

	# 验证协议版本
	if data.get("protocol_version") != "1.0":
		push_error("不支持的关卡协议版本。")
		return false

	# 验证关卡 ID
	if typeof(data.get("level_id")) != TYPE_STRING:
		push_error("关卡 level_id 必须是字符串。")
		return false

	if data["level_id"].is_empty():
		push_error("关卡 level_id 不能为空。")
		return false

	# 验证关卡名称
	if typeof(data.get("name")) != TYPE_STRING:
		push_error("关卡 name 必须是字符串。")
		return false

	if data["name"].is_empty():
		push_error("关卡 name 不能为空。")
		return false

	# 验证描述
	if data.has("description"):
		if typeof(data["description"]) != TYPE_STRING:
			push_error("关卡 description 必须是字符串。")
			return false

	# 验证坐标系统
	if data.get("coordinate_system") != "cartesian_y_up":
		push_error("不支持的坐标系统。")
		return false

	# 验证地图宽度
	if not is_integer_number(data.get("width")):
		push_error("地图 width 必须是整数。")
		return false

	# 验证地图高度
	if not is_integer_number(data.get("height")):
		push_error("地图 height 必须是整数。")
		return false

	var width: int = int(data["width"])
	var height: int = int(data["height"])

	if width < 1 or width > 1000:
		push_error("地图宽度必须在 1 到 1000 之间。")
		return false

	if height < 1 or height > 1000:
		push_error("地图高度必须在 1 到 1000 之间。")
		return false

	# 验证单元格大小
	if not is_finite_number(data.get("cell_size")):
		push_error("cell_size 必须是有限数字。")
		return false

	if float(data["cell_size"]) <= 0.0:
		push_error("cell_size 必须大于 0。")
		return false

	# 验证实体列表
	if typeof(data.get("entities")) != TYPE_ARRAY:
		push_error("关卡 entities 必须是数组。")
		return false

	var entities: Array = data["entities"]

	# 用于检查实体 ID 是否重复
	var seen_ids: Dictionary = {}

	# 允许的实体字段
	var allowed_fields = [
		"id",
		"type",
		"position",
		"direction",
		"rotation",
		"layer",
		"asset_id",
		"properties"
	]

	# 逐个验证实体
	for entity in entities:

		if not (entity is Dictionary):
			push_error("实体必须是 JSON 对象。")
			return false

		# 检查是否存在未定义字段
		for key in entity.keys():
			if not allowed_fields.has(key):
				push_error("实体包含未知字段：" + str(key))
				return false

		# 验证实体 ID
		if typeof(entity.get("id")) != TYPE_STRING:
			push_error("实体缺少有效的 id。")
			return false

		var entity_id: String = entity["id"]

		if entity_id.is_empty():
			push_error("实体 id 不能为空。")
			return false

		# 检查 ID 唯一性
		if seen_ids.has(entity_id):
			push_error("发现重复实体 ID：" + entity_id)
			return false

		seen_ids[entity_id] = true

		# 验证实体类型
		if typeof(entity.get("type")) != TYPE_STRING:
			push_error("实体缺少有效的 type。")
			return false

		if entity["type"].is_empty():
			push_error("实体 type 不能为空。")
			return false

		# 验证坐标对象
		if not (entity.get("position") is Dictionary):
			push_error("实体 position 必须是对象。")
			return false

		var entity_position: Dictionary = entity["position"]

		if entity_position.has("x") == false or entity_position.has("y") == false:
			push_error("实体 position 必须包含 x 和 y。")
			return false

		for position_key in entity_position.keys():
			if position_key != "x" and position_key != "y":
				push_error("position 包含未知字段：" + str(position_key))
				return false

		# 验证坐标
		if not is_integer_number(entity_position.get("x")):
			push_error("实体坐标 x 必须是整数。")
			return false

		if not is_integer_number(entity_position.get("y")):
			push_error("实体坐标 y 必须是整数。")
			return false

		var x: int = int(entity_position["x"])
		var y: int = int(entity_position["y"])

		if x < 0 or x >= width:
			push_error("实体 x 坐标超出地图范围。")
			return false

		if y < 0 or y >= height:
			push_error("实体 y 坐标超出地图范围。")
			return false

		# 验证方向字段
		if entity.has("direction"):
			if entity["direction"] != null:
				if typeof(entity["direction"]) != TYPE_STRING:
					push_error("实体 direction 必须是字符串或 null。")
					return false

		# 验证旋转角度
		if entity.has("rotation"):
			if not is_finite_number(entity["rotation"]):
				push_error("实体 rotation 必须是有限数字。")
				return false

		# 验证图层
		if entity.has("layer"):
			if typeof(entity["layer"]) != TYPE_STRING:
				push_error("实体 layer 必须是字符串。")
				return false

			if entity["layer"].is_empty():
				push_error("实体 layer 不能为空。")
				return false

		# 验证资源 ID
		if entity.has("asset_id"):
			if entity["asset_id"] != null:
				if typeof(entity["asset_id"]) != TYPE_STRING:
					push_error("实体 asset_id 必须是字符串或 null。")
					return false

		# 验证自定义属性
		if entity.has("properties"):
			if not (entity["properties"] is Dictionary):
				push_error("实体 properties 必须是对象。")
				return false

	return true
