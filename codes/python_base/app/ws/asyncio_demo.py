import asyncio
import time

# 1. 定义协程 (Coroutine)
# 使用 async def 声明，告诉 Python 该函数是一个可以“挂起”的协程
async def fetch_api_data(service_name: str, delay: int):
    print(f"[{service_name}] 开始请求数据... (预计耗时 {delay}s)")
    
    # 2. 模拟非阻塞 I/O (Await)
    # await 会将控制权交还给事件循环 (Event Loop)，CPU 不会在此死等
    # 在实际工程中，这里通常是使用 httpx 发起网络请求
    await asyncio.sleep(delay) 
    
    print(f"[{service_name}] 数据获取成功！")
    return {"service": service_name, "status": "success"}

async def main():
    start_time = time.perf_counter()
    print(">>> 启动异步并发任务")

    # 3. 任务调度 (Concurrency)
    # asyncio.gather 会将多个协程封装成任务并同时提交给事件循环
    task1 = fetch_api_data("用户服务", 3)
    task2 = fetch_api_data("订单服务", 2)
    
    # 并发执行并等待所有结果返回
    results = await asyncio.gather(task1, task2)

    end_time = time.perf_counter()
    print(f"\n任务完成：{results}")
    # 深度解析：总耗时仅为 3 秒（最长任务时间），而非 3+2=5 秒
    print(f"总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    # 启动事件循环，这是异步程序的引擎 
    # asyncio 的本质是一个无限循环，它持续监控注册在其上的所有任务状态。
    # 当 main() 中调用 asyncio.gather 时，任务被加入队列，指挥官开始调度执行。
    asyncio.run(main()) 