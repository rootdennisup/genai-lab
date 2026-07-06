import pytest
from app.ws.math_tool import divide, save_result

# --- 场景 1: 基础断言 ---
def test_divide_success():
    # pytest 详尽的断言内省机制允许直接使用普通 assert [1]
    # 无需记忆 unittest 中繁琐的 self.assertEqual() [1]
    assert divide(10, 2) == 5.0
    assert divide(5, 2) == 2.5

# --- 场景 2: 异常捕获 ---
def test_divide_zero_exception():
    # 使用 pytest.raises 装饰器断言代码是否正确抛出预期异常 [3, 4]
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    # 还可以校验异常的具体信息
    assert "除数不能为零" in str(excinfo.value)

# --- 场景 3: 使用内置 Fixtures 管理资源 ---
def test_save_result_to_file(tmp_path):
    # tmp_path 是 pytest 内置的 Fixture，用于创建测试完即销毁的临时目录 [5, 6]
    # 它返回一个 pathlib.Path 对象，具有极佳的跨平台兼容性 [6, 7]
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "result.txt"
    
    save_result(file_path, 42)
    
    # 校验文件是否正确写入
    assert file_path.read_text() == "42"