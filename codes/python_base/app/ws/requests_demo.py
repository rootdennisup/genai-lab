import requests
import httpx

# requests 方式
res_req = requests.get("https://fastapi.tiangolo.com/zh/", timeout=5.0)

# httpx 同步方式 (几乎无缝切换)
with httpx.Client() as client:
    res_hpx = client.get("https://fastapi.tiangolo.com/zh/", timeout=5.0)

# httpx 的同步接口与 requests 几乎完全一致，这使得从旧库迁移极其容易。