#!/usr/bin/env python3
"""
智能图像检测服务器启动脚本
"""
import os
import sys

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import app


def main():
    """主函数"""
    print("=" * 50)
    print("智能图像检测服务器")
    print("=" * 50)
    print(f"访问地址: http://localhost:5000")
    print("接口文档:")
    print("  GET  /health      - 健康检查")
    print("  GET  /model_info  - 模型信息")
    print("  POST /detect      - 图像检测")
    print("=" * 50)

    # 启动服务器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


if __name__ == '__main__':
    main()