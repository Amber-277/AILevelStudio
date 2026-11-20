
@tool
extends Node2D


const GENERATED_NODE_NAME = "GeneratedLevel"
const GENERATED_META_KEY = "ai_level_studio_generated"

const LevelValidator = preload("res://scripts/level_validator.gd")
const LevelGenerator = preload("res://scripts/level_generator.gd")


# 接收插件传入的关卡数据
func load_level(level_data: Dictionary) -> bool:

	# 第一步：创建验证器
	var validator = LevelValidator.new()

	if validator == null:
		push_error("无法创建关卡验证器！")
		return false

	# 第二步：验证数据
	if not validator.validate_level_data(level_data):
		push_error("关卡数据验证失败，保留原有地图。")
		return false

	# 第三步：检查旧生成容器
	var old_generated = get_node_or_null(GENERATED_NODE_NAME)

	if old_generated != null:

		if not old_generated.has_meta(GENERATED_META_KEY):
			push_error("发现同名节点，但它不是 AI Level Studio 生成的节点。")
			return false

		if old_generated.get_meta(GENERATED_META_KEY) != true:
			push_error("生成容器标记异常，取消导入。")
			return false

	# 第四步：创建生成器
	var generator = LevelGenerator.new()

	if generator == null:
		push_error("无法创建关卡生成器！")
		return false

	# 第五步：在场景外创建新地图
	var new_generated: Node2D = generator.generate_level(level_data)

	if new_generated == null:
		push_error("新地图生成失败，保留原有地图。")
		return false

	# 第六步：移除旧地图
	if old_generated != null:
		remove_child(old_generated)
		old_generated.free()

	# 第七步：将新地图加入场景
	add_child(new_generated)

	# 第八步：设置场景所有者
	set_owner_recursive(new_generated, self)

	# 调试信息：检查节点是否真正加入场景
	print("当前根节点子节点数量：", get_child_count())
	print("生成节点是否加入场景树：", new_generated.is_inside_tree())
	print("生成节点 Owner：", new_generated.owner)

	print("关卡导入成功！")
	return true


# 递归设置场景所有者
func set_owner_recursive(node: Node, scene_owner: Node) -> void:

	node.owner = scene_owner

	for child in node.get_children():
		set_owner_recursive(child, scene_owner)
