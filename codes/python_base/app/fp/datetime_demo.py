from datetime import datetime, timedelta, timezone

# 1. 获取当前本地时间
now = datetime.now()
print(f"当前本地时间: {now}")

# 2. 格式化输出 (strftime)
# 将时间对象转为人类易读的字符串
fmt_str = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化后的时间: {fmt_str}")

# 3. 字符串解析 (strptime)
# 将字符串转回时间对象
date_obj = datetime.strptime("2026-01-01", "%Y-%m-%d")
print(f"解析后的对象: {date_obj}")

# 4. 时间加减运算 (timedelta)
# 模拟计算 7 天前的时间点
seven_days_ago = now - timedelta(days=7)
print(f"7 天前是: {seven_days_ago}")

# 5. 时区处理 (现代 Python 推荐方式)
# 获取当前的 UTC 时间
utc_now = datetime.now(timezone.utc)
print(f"当前 UTC 时间: {utc_now}")