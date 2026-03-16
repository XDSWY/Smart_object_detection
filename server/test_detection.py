import requests
import os


def test_detection():
    """测试图片检测功能"""
    url = "http://127.0.0.1:5000/detect"

    # 使用本地图片测试
    image_path = "test_image.jpg"

    # 如果没有测试图片，先创建一个简单的测试
    if not os.path.exists(image_path):
        print("请准备一张测试图片，命名为 test_image.jpg 放在 server 文件夹中")
        print("或者用手机拍一张包含人、车、猫、狗等的照片传到电脑")
        return

    try:
        # 发送检测请求
        with open(image_path, 'rb') as f:
            files = {'image': (image_path, f, 'image/jpeg')}
            result = requests.post(url, files=files)

        print("检测结果:")
        print(result.json())
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    test_detection()