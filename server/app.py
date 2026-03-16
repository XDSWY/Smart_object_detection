from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import logging
from config import config
from utils.helpers import allowed_file, get_object_descriptions
import io
from PIL import Image
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config['development'])

# 更完善的CORS配置
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8000", "http://192.168.*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "max_age": 3600
    }
})


# 或者简单使用（开发环境）
# CORS(app, supports_credentials=True)

# 添加处理OPTIONS请求的通用方法
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# 全局变量
model = None
object_descriptions = {}


def init_model():
    """初始化YOLO模型"""
    global model
    try:
        logger.info("正在加载YOLO模型...")
        model = YOLO('yolov8n.pt')  # 使用更小的模型
        logger.info("模型加载成功!")
        return True
    except Exception as e:
        logger.error(f"模型加载失败: {str(e)}")
        return False


def init_descriptions():
    """初始化物体描述信息"""
    global object_descriptions
    object_descriptions = get_object_descriptions()
    logger.info("物体描述信息加载完成!")
    return True


# 应用启动时初始化
logger.info("初始化应用...")
init_model()
init_descriptions()


@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '智能图像检测API服务',
        'version': '1.0.0',
        'endpoints': {
            '/detect': 'POST - 图像检测',
            '/health': 'GET - 健康检查',
            '/model_info': 'GET - 模型信息',
            '/test': 'GET - 测试连接'
        }
    })


@app.route('/detect', methods=['POST', 'OPTIONS'])
def detect_objects():
    """物体检测接口"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    try:
        logger.info("=== 开始处理检测请求 ===")

        if 'image' not in request.files:
            logger.error("未找到image字段")
            return jsonify({
                'success': False,
                'error': '未提供图片文件'
            }), 400

        image_file = request.files['image']
        logger.info(f"收到文件: {image_file.filename}")

        # 读取图片数据
        image_data = image_file.read()
        logger.info(f"图片大小: {len(image_data)} 字节")

        if len(image_data) == 0:
            logger.error("图片数据为空")
            return jsonify({
                'success': False,
                'error': '图片数据为空'
            }), 400

        # 验证并保存图片
        try:
            image = Image.open(io.BytesIO(image_data))
            logger.info(f"图片格式: {image.format}, 尺寸: {image.size}")
        except Exception as e:
            logger.error(f"图片打开失败: {str(e)}")
            return jsonify({
                'success': False,
                'error': '无效的图片文件'
            }), 400

        # 保存临时文件
        temp_path = "temp_image.jpg"
        image.save(temp_path)
        logger.info(f"临时文件保存成功")

        # 执行物体检测
        logger.info("开始YOLO模型检测...")
        results = model(temp_path)
        logger.info(f"YOLO检测完成，返回 {len(results)} 个结果")

        # 解析检测结果
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])

                # 获取详细描述信息
                obj_info = object_descriptions.get(class_name, {})
                logger.info(f"物体: {class_name}, 描述信息: {obj_info}")

                detection_info = {
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': box.xyxy[0].tolist(),
                    'category': obj_info.get('category', '未知类别'),
                    'description': obj_info.get('description', f'检测到物体: {class_name}'),
                    'features': obj_info.get('features', '暂无特征信息'),
                    'additional_info': obj_info.get('breeds') or obj_info.get('types') or obj_info.get(
                        'habitat') or obj_info.get('origin') or obj_info.get('materials') or obj_info.get(
                        'usage') or obj_info.get('lifespan') or obj_info.get('nutrition') or obj_info.get(
                        'species') or obj_info.get('varieties') or obj_info.get('behavior') or '暂无额外信息'
                }
                logger.info(f"最终检测信息: {detection_info}")
                detections.append(detection_info)

        logger.info(f"检测完成，共发现 {len(detections)} 个物体")

        # 按置信度排序
        detections.sort(key=lambda x: x['confidence'], reverse=True)

        return jsonify({
            'success': True,
            'detections': detections,
            'count': len(detections),
            'message': f'成功检测到 {len(detections)} 个物体'
        })

    except Exception as e:
        logger.error(f"检测过程中出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': '检测失败',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    health_status = {
        'status': 'healthy',
        'service': '智能图像检测API',
        'model_loaded': model is not None,
        'descriptions_loaded': len(object_descriptions) > 0,
        'timestamp': os.times().user
    }
    return jsonify(health_status)


@app.route('/test', methods=['GET'])
def test_connection():
    """测试连接接口"""
    return jsonify({
        'success': True,
        'message': '连接成功!',
        'timestamp': os.times().user
    })


@app.route('/model_info', methods=['GET'])
def model_info():
    """模型信息接口"""
    if model is None:
        return jsonify({
            'success': False,
            'error': '模型未加载'
        }), 500

    return jsonify({
        'success': True,
        'model_name': 'YOLOv8n',
        'classes_count': len(model.names),
        'descriptions_count': len(object_descriptions)
    })


@app.route('/test_upload', methods=['POST'])
def test_upload():
    """测试图片上传接口"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image'}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'success': False, 'error': 'Empty filename'}), 400

        # 读取图片基本信息
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))

        return jsonify({
            'success': True,
            'message': 'Upload test successful',
            'file_size': len(image_data),
            'image_format': image.format,
            'image_size': image.size
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/quick_test', methods=['POST'])
def quick_test():
    """快速测试接口 - 不进行实际检测"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image'}), 400

        image_file = request.files['image']
        image_data = image_file.read()

        # 模拟处理时间
        import time
        time.sleep(2)

        return jsonify({
            'success': True,
            'message': '快速测试成功',
            'file_size': len(image_data),
            'test_detections': [
                {
                    'class': 'person',
                    'confidence': 0.95,
                    'description': '👤 人类 - 测试数据'
                }
            ]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # 启动服务器
    logger.info(f"启动服务器: http://{app.config['HOST']}:{app.config['PORT']}")
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=True,  # 暂时开启debug以便查看错误
        use_reloader=False
    )