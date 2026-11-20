
@tool
extends EditorPlugin


const MENU_ITEM_NAME = "导入 AI Level Studio 关卡"
const PREVIEW_SCENE_PATH = "res://scenes/level_preview.tscn"

var file_dialog: FileDialog


func _enter_tree() -> void:
    file_dialog = FileDialog.new()
    file_dialog.title = "选择 AI Level Studio 关卡"
    file_dialog.file_mode = FileDialog.FILE_MODE_OPEN_FILE
    file_dialog.access = FileDialog.ACCESS_FILESYSTEM
    file_dialog.filters = PackedStringArray([
        "*.json ; JSON 关卡文件"
    ])

    file_dialog.file_selected.connect(_on_file_selected)

    get_editor_interface().get_base_control().add_child(file_dialog)

    add_tool_menu_item(MENU_ITEM_NAME, _on_import_level)

    print("AI Level Studio 插件已启用！")


func _exit_tree() -> void:
    remove_tool_menu_item(MENU_ITEM_NAME)

    if is_instance_valid(file_dialog):
        file_dialog.queue_free()

    print("AI Level Studio 插件已关闭！")


func _on_import_level() -> void:
    file_dialog.popup_centered(Vector2i(900, 600))


func _on_file_selected(path: String) -> void:
    print("选择的关卡文件：", path)

    # 读取 JSON 文件
    var file = FileAccess.open(path, FileAccess.READ)

    if file == null:
        push_error("无法打开关卡文件！")
        return

    var json_text = file.get_as_text()
    file.close()

    # 解析 JSON
    var json = JSON.new()
    var error = json.parse(json_text)

    if error != OK:
        push_error("JSON 解析失败：" + json.get_error_message())
        return

    var level_data = json.data

    if typeof(level_data) != TYPE_DICTIONARY:
        push_error("关卡 JSON 的最外层必须是对象！")
        return

    # 获取当前打开的场景
    var edited_scene_root = get_editor_interface().get_edited_scene_root()

    if edited_scene_root == null:
        push_error("当前没有打开的场景！")
        return

    # 调用场景脚本中的 load_level 函数
    if not edited_scene_root.has_method("load_level"):
        push_error("当前场景没有 load_level 函数！")
        return

    edited_scene_root.load_level(level_data)

    print("关卡数据已传递给场景！")
