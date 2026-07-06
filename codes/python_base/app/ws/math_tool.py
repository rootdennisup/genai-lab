def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def save_result(path, result):
    with open(path, "w") as f:
        f.write(str(result))