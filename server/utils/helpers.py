def allowed_file(filename):
    """检查文件扩展名是否允许"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_object_descriptions():
    """获取详细的物体描述信息"""
    return {
        "person": {
            "category": "人类",
            "description": "👤 人类 - 具有直立行走和使用工具能力的高级哺乳动物。",
            "features": "具有高度发达的大脑、语言能力和复杂的社会结构。",
            "habitat": "全球分布，适应各种环境"
        },
        "car": {
            "category": "交通工具",
            "description": "🚗 汽车 - 四轮机动车辆，用于人员和货物运输。",
            "features": "通常由内燃机或电动机驱动，具有转向、制动和悬挂系统。",
            "types": "轿车、SUV、卡车、跑车等"
        },
        "cat": {
            "category": "哺乳动物",
            "description": "🐱 猫 - 小型猫科动物，常见的家庭宠物。",
            "features": "夜行性动物，具有敏锐的听觉和视觉，爪子可伸缩。",
            "breeds": "波斯猫、暹罗猫、英国短毛猫、布偶猫等",
            "behavior": "独立、好奇、喜欢清洁"
        },
        "dog": {
            "category": "哺乳动物",
            "description": "🐶 狗 - 犬科动物，人类最忠诚的伙伴。",
            "features": "嗅觉极其灵敏，听觉范围广，具有强烈的社会性。",
            "breeds": "金毛寻回犬、哈士奇、柯基、泰迪等",
            "lifespan": "10-13年"
        },
        "bicycle": {
            "category": "交通工具",
            "description": "🚲 自行车 - 两轮交通工具，环保且有助于锻炼身体。",
            "features": "人力驱动，通过脚踏板传动，具有链条和齿轮系统。",
            "types": "山地车、公路车、折叠车、城市通勤车"
        },
        "motorcycle": {
            "category": "交通工具",
            "description": "🏍️ 摩托车 - 两轮机动车辆，具有灵活性和速度。",
            "features": "由发动机驱动，具有较高的功率重量比。",
            "types": "街车、跑车、巡航车、越野车"
        },
        "cell phone": {
            "category": "电子设备",
            "description": "📱 手机 - 便携式通信设备。",
            "features": "具有通话、短信、上网、拍照等多种功能。",
            "types": "智能手机、功能手机"
        },
        "laptop": {
            "category": "电子设备",
            "description": "💻 笔记本电脑 - 便携式个人电脑。",
            "features": "集成显示器、键盘、电池，便于携带和使用。",
            "usage": "办公、学习、娱乐、编程等"
        },
        "book": {
            "category": "文化用品",
            "description": "📚 书籍 - 用于记录和传播知识的印刷品。",
            "features": "由纸张和封面组成，包含文字和/或图片。",
            "types": "小说、教科书、杂志、漫画等"
        },
        "chair": {
            "category": "家具",
            "description": "🪑 椅子 - 带有靠背的坐具。",
            "features": "提供坐姿支撑，通常有腿和靠背。",
            "materials": "木材、金属、塑料、布料等"
        },
        "bird": {
            "category": "鸟类",
            "description": "🐦 鸟类 - 有羽毛、翅膀和喙的脊椎动物。",
            "features": "大多数会飞行，产卵，具有轻质的骨骼。",
            "species": "麻雀、鸽子、鹦鹉、鹰等"
        },
        "bottle": {
            "category": "容器",
            "description": "🍶 瓶子 - 用于盛装液体的容器。",
            "features": "通常有颈部，口部较小，便于倾倒液体。",
            "materials": "玻璃、塑料、陶瓷、金属"
        },
        "cup": {
            "category": "餐具",
            "description": "☕ 杯子 - 用于饮用液体的开口容器。",
            "features": "通常有手柄，容量较小，便于手持。",
            "types": "咖啡杯、茶杯、马克杯、玻璃杯"
        },
        "apple": {
            "category": "水果",
            "description": "🍎 苹果 - 蔷薇科苹果属植物的果实。",
            "features": "圆形，果皮颜色多样，果肉清脆多汁。",
            "varieties": "红富士、嘎啦果、蛇果、青苹果等",
            "nutrition": "富含维生素C和膳食纤维"
        },
        "banana": {
            "category": "水果",
            "description": "🍌 香蕉 - 芭蕉科植物的果实。",
            "features": "弯曲的长形果实，果皮黄色，果肉柔软香甜。",
            "origin": "原产于东南亚，现广泛种植于热带地区"
        }
    }