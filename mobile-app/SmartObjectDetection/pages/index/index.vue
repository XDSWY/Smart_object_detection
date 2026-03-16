<template>
	<view class="container">
		<!-- 头部 -->
		<view class="header">
			<!-- 添加Logo图片 -->
			<view class="logo-container">
				<image class="logo-image" src="/static/images/logo.jpg" mode="aspectFit"></image>
			</view>
			<text class="company-name">AI视觉科技</text>
			<text class="app-title">智能图像检测</text>
		</view>
		
		<!-- 功能按钮 -->
		<view class="button-group">
			<button class="action-btn primary" @tap="takePhoto">
				<text class="btn-icon">📷</text>
				<text class="btn-text">拍照检测</text>
			</button>
			
			<button class="action-btn secondary" @tap="chooseImage">
				<text class="btn-icon">🖼️</text>
				<text class="btn-text">从相册选择</text>
			</button>
			
			<button class="action-btn light" @tap="gotoAbout">
				<text class="btn-icon">ℹ️</text>
				<text class="btn-text">关于我们</text>
			</button>
		</view>
		
		<!-- 服务器状态 -->
		<view class="status-info">
			<text class="status-text">服务器状态: {{ serverStatus }}</text>
		</view>
	</view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const serverStatus = ref('检查中...')

// 检查服务器状态
// 检查服务器状态
// 检查服务器状态
const checkServerStatus = async () => {
    const testUrls = [
        '/api/health',  // 代理连接
        'http://127.0.0.1:5000/health',  // 直接连接
        'http://localhost:5000/health'   // 本地连接
    ];
    
    for (let i = 0; i < testUrls.length; i++) {
        try {
            console.log(`尝试连接: ${testUrls[i]}`);
            const response = await uni.request({
                url: testUrls[i],
                method: 'GET',
                timeout: 3000
            });
            
            console.log('响应数据:', response);
            
            if (response.data.status === 'healthy') {
                serverStatus.value = `在线 ✅`;
                console.log(`连接成功: ${testUrls[i]}`);
                return;
            }
        } catch (error) {
            console.log(`连接失败 ${testUrls[i]}:`, error.errMsg);
        }
    }
    
    serverStatus.value = '离线 ❌';
    uni.showToast({
        title: '无法连接到服务器',
        icon: 'none'
    });
};

// 拍照功能
const takePhoto = () => {
	uni.chooseImage({
		count: 1,
		sourceType: ['camera'],
		success: (res) => {
			uploadImage(res.tempFilePaths[0])
		},
		fail: (error) => {
			uni.showToast({
				title: '拍照失败',
				icon: 'none'
			})
		}
	})
}

// 选择相册图片
const chooseImage = () => {
	uni.chooseImage({
		count: 1,
		sourceType: ['album'],
		success: (res) => {
			uploadImage(res.tempFilePaths[0])
		},
		fail: (error) => {
			uni.showToast({
				title: '选择图片失败',
				icon: 'none'
			})
		}
	})
}

// 上传图片到服务器
const uploadImage = async (filePath) => {
    console.log('开始上传图片:', filePath)
    
    uni.showLoading({
        title: '检测中...',
        mask: true
    })
    
    try {
        // 使用直接连接
        const backendUrl = 'http://127.0.0.1:5000/detect'
        console.log('使用后端URL:', backendUrl)
        
        const response = await uni.uploadFile({
            url: backendUrl,
            filePath: filePath,
            name: 'image',
            formData: {
                'type': 'detect'
            },
            timeout: 30000
        })
        
        console.log('完整响应对象:', response)
        console.log('状态码:', response.statusCode)
        console.log('响应数据:', response.data)
        
        uni.hideLoading()
        
        if (response.statusCode === 200) {
            console.log('请求成功，准备解析数据')
            
            let result
            try {
                // 注意：uni.uploadFile 返回的 data 已经是字符串，不需要再 parse
                if (typeof response.data === 'string') {
                    result = JSON.parse(response.data)
                } else {
                    result = response.data
                }
                console.log('解析后的结果:', result)
            } catch (parseError) {
                console.error('JSON解析错误:', parseError)
                console.error('原始数据:', response.data)
                uni.showToast({
                    title: '响应数据格式错误',
                    icon: 'none',
                    duration: 3000
                })
                return
            }
            
            if (result.success) {
                console.log('检测成功，准备跳转')
                
                // 对参数进行编码
                const resultData = encodeURIComponent(JSON.stringify(result))
                const imagePath = encodeURIComponent(filePath)
                
                console.log('跳转参数准备完成')
                
                // 先尝试使用 redirectTo
                uni.redirectTo({
                    url: `/pages/result/result?data=${resultData}&imagePath=${imagePath}`,
                    success: () => {
                        console.log('redirectTo跳转到结果页面成功')
                    },
                    fail: (error) => {
                        console.error('redirectTo跳转失败:', error)
                        console.log('尝试使用navigateTo...')
                        
                        // 如果redirectTo失败，尝试navigateTo
                        uni.navigateTo({
                            url: `/pages/result/result?data=${resultData}&imagePath=${imagePath}`,
                            success: () => {
                                console.log('navigateTo跳转到结果页面成功')
                            },
                            fail: (error2) => {
                                console.error('navigateTo也失败:', error2)
                                
                                // 如果所有跳转都失败，显示临时结果
                                // 如果所有跳转都失败，显示临时结果
                                console.log('显示临时结果')
                                const detectionText = result.detections.map(item => 
                                    `【${item.class}】\n` +
                                    `置信度: ${(item.confidence * 100).toFixed(1)}%\n` +
                                    `类别: ${item.category || '未知'}\n` +
                                    `描述: ${item.description || '无描述'}\n` +
                                    `特征: ${item.features || '无特征信息'}\n` +
                                    `详细信息: ${item.additional_info || '无额外信息'}`
                                ).join('\n\n')
                                
                                uni.showModal({
                                    title: `检测结果 - 发现 ${result.count} 个物体`,
                                    content: detectionText,
                                    showCancel: false,
                                    confirmText: '确定',
                                    success: (res) => {
                                        if (res.confirm) {
                                            console.log('用户查看了临时结果')
                                        }
                                    }
                                })
                            }
                        })
                    }
                })
            } else {
                console.log('检测失败:', result.error)
                uni.showToast({
                    title: result.error || '检测失败',
                    icon: 'none',
                    duration: 3000
                })
            }
        } else {
            console.error('服务器返回错误状态码:', response.statusCode)
            let errorMsg = '服务器错误'
            try {
                const errorData = JSON.parse(response.data)
                errorMsg = errorData.error || errorData.message || errorMsg
            } catch (e) {
                // 忽略解析错误
            }
            
            uni.showToast({
                title: `${errorMsg} (状态码: ${response.statusCode})`,
                icon: 'none',
                duration: 4000
            })
        }
    } catch (error) {
        uni.hideLoading()
        console.error('上传失败:', error)
        console.error('错误详情:', error.errMsg)
        uni.showToast({
            title: `请求失败: ${error.errMsg || '未知错误'}`,
            icon: 'none',
            duration: 3000
        })
    }
}



// 跳转到关于页面 - 修改为显示弹窗
const gotoAbout = () => {
    uni.showModal({
        title: '关于我们',
        content: '智能图像检测应用\n\n🔍 基于YOLOv8深度学习模型\n📱 支持拍照和相册选择\n🚀 实时物体检测与识别\n🔄 支持80+种常见物体\n\n版本: v1.0.0\n开发时间: 2025年',
        showCancel: false,
        confirmText: '确定',
        confirmColor: '#007AFF'
    })
}


// 测试页面跳转
const testJump = () => {
    console.log('测试跳转')
    // 直接跳转，不添加任何错误处理
    uni.navigateTo({
        url: '/pages/about/about'
    })
}

// 使用 onMounted 替代 onLoad
onMounted(() => {
    checkServerStatus()
    
    // 调试路由信息
    console.log('=== 路由调试信息 ===')
    console.log('当前页面栈:', getCurrentPages())
    console.log('about页面路径:', '/pages/about/about')
    console.log('result页面路径:', '/pages/result/result')
})
</script>

<style scoped>
/* Logo容器样式 */
.logo-container {
	width: 200rpx;
	height: 200rpx;
	margin: 0 auto 30rpx auto;
	background: white;
	border-radius: 40rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
	padding: 20rpx;
}

/* Logo图片样式 */
.logo-image {
	width: 160rpx;
	height: 160rpx;
	border-radius: 30rpx;
}

.container {
	padding: 40rpx;
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	display: flex;
	flex-direction: column;
	align-items: center;
}

.header {
	text-align: center;
	margin-bottom: 80rpx;
	margin-top: 60rpx;
}

.logo {
	width: 160rpx;
	height: 160rpx;
	border-radius: 40rpx;
	background: white;
	padding: 20rpx;
	margin-bottom: 30rpx;
}

.company-name {
	display: block;
	font-size: 32rpx;
	color: white;
	opacity: 0.9;
	margin-bottom: 10rpx;
}

.app-title {
	display: block;
	font-size: 48rpx;
	color: white;
	font-weight: bold;
}

.button-group {
	width: 100%;
	max-width: 600rpx;
}

.action-btn {
	width: 100%;
	height: 120rpx;
	border-radius: 20rpx;
	margin-bottom: 30rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	border: none;
	font-size: 36rpx;
	transition: all 0.3s;
}

.action-btn:active {
	transform: scale(0.98);
}

.primary {
	background: #007AFF;
	color: white;
}

.secondary {
	background: #5856D6;
	color: white;
}

.light {
	background: rgba(255, 255, 255, 0.2);
	color: white;
	backdrop-filter: blur(10px);
}

.btn-icon {
	margin-right: 20rpx;
	font-size: 44rpx;
}

.btn-text {
	font-weight: 500;
}

.status-info {
	margin-top: 60rpx;
	padding: 20rpx 40rpx;
	background: rgba(255, 255, 255, 0.1);
	border-radius: 50rpx;
	backdrop-filter: blur(10px);
}

.status-text {
	color: white;
	font-size: 28rpx;
	opacity: 0.8;
}
</style>