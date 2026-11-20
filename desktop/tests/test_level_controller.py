
import json

import pytest

from desktop.app.controllers.level_controller import LevelController


@pytest.fixture
def controller():
	return LevelController()


@pytest.fixture
def valid_level_json():
	return json.dumps({
		"protocol_version": "1.0",
		"level_id": "controller_test",
		"name": "Controller 测试关卡",
		"description": "用于测试控制器",
		"width": 10,
		"height": 8,
		"cell_size": 1.0,
		"coordinate_system": "cartesian_y_up",
		"entities": [
			{
				"id": "wall_001",
				"type": "wall",
				"position": {
					"x": 2,
					"y": 3
				}
			}
		]
	}, ensure_ascii=False)


# 测试 1：正常 JSON 能否解析
def test_parse_valid_level(controller, valid_level_json):

	level = controller.parse_level(valid_level_json)

	assert level.level_id == "controller_test"
	assert level.name == "Controller 测试关卡"
	assert level.width == 10
	assert len(level.entities) == 1


# 测试 2：错误 JSON 能否被拒绝
def test_reject_invalid_json(controller):

	invalid_json = '{"level_id": "broken", "width": }'

	with pytest.raises(ValueError):
		controller.parse_level(invalid_json)


# 测试 3：能否发现关卡规则问题
def test_detect_level_rule_issues(controller):

	json_text = json.dumps({
		"protocol_version": "1.0",
		"level_id": "invalid_position",
		"name": "越界测试",
		"width": 5,
		"height": 5,
		"cell_size": 1.0,
		"coordinate_system": "cartesian_y_up",
		"entities": [
			{
				"id": "wall_001",
				"type": "wall",
				"position": {
					"x": 8,
					"y": 2
				}
			}
		]
	})

	level, issues = controller.validate_json(json_text)

	assert level.level_id == "invalid_position"
	assert len(issues) == 1
	assert issues[0].code == "POSITION_OUT_OF_BOUNDS"


# 测试 4：有规则错误的关卡不能保存
def test_reject_save_with_rule_issues(controller, tmp_path):

	json_text = json.dumps({
		"protocol_version": "1.0",
		"level_id": "invalid_save",
		"name": "禁止保存测试",
		"width": 5,
		"height": 5,
		"cell_size": 1.0,
		"coordinate_system": "cartesian_y_up",
		"entities": [
			{
				"id": "wall_001",
				"type": "wall",
				"position": {
					"x": 8,
					"y": 2
				}
			}
		]
	})

	level = controller.parse_level(json_text)
	file_path = tmp_path / "invalid_level.json"

	with pytest.raises(ValueError, match="关卡存在规则问题"):
		controller.save_level(level, file_path)

	assert not file_path.exists()


# 测试 5：正常关卡能否保存并重新读取
def test_save_and_open_level(controller, valid_level_json, tmp_path):

	level = controller.parse_level(valid_level_json)

	file_path = tmp_path / "valid_level.json"

	controller.save_level(level, file_path)

	assert file_path.exists()

	loaded_level = controller.open_level(file_path)

	assert loaded_level.level_id == level.level_id
	assert loaded_level.name == level.name
	assert loaded_level.width == level.width
	assert len(loaded_level.entities) == 1
