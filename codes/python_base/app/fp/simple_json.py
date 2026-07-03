import json

# 内存中的 Python 数据结构
config_data = {
    "app_name": "MyPythonTool",
    "version": 1.0,
    "settings": ["auto_save", "debug_mode"]
}

# 序列化：将数据保存到本地文件
with open('tmp/config.json', 'w', encoding='utf-8') as f:
    # 使用 json.dump 保存结构化数据 
    json.dump(config_data, f, indent=4)

# 反序列化：从文件中读取数据
with open('tmp/config.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)
    print(f"应用名称: {loaded_data['app_name']}")