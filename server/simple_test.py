import requests

def simple_test():
    """简单测试连接"""
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        print("连接成功!")
        print(response.json())
    except Exception as e:
        print(f"连接失败: {e}")

if __name__ == "__main__":
    simple_test()