<template>
	<view class="container">
		<!-- 头部 -->
		<view class="header">
			<text class="title">检测结果</text>
			<text class="subtitle" v-if="resultData">{{ resultData.count }} 个物体被检测到</text>
		</view>
		
		<!-- 原图显示 -->
		<view class="image-section" v-if="imagePath">
			<image class="preview-image" :src="imagePath" mode="widthFix"></image>
		</view>
		
		<!-- 检测结果列表 -->
		<view class="results-section" v-if="resultData && resultData.detections.length > 0">
		    <view class="result-item" v-for="(item, index) in resultData.detections" :key="index">
		        <view class="item-header">
		            <text class="object-name">{{ item.class }}</text>
		            <text class="confidence">{{ (item.confidence * 100).toFixed(1) }}%</text>
		        </view>
		        
		        <!-- 类别信息 -->
		        <view class="category-info" v-if="item.category">
		            <text class="category-label">类别: {{ item.category }}</text>
		        </view>
		        
		        <!-- 物体描述 -->
		        <view class="item-description" v-if="item.description">
		            {{ item.description }}
		        </view>
		        
		        <!-- 主要特征 -->
		        <view class="features-info" v-if="item.features">
		            <text class="features-title">主要特征:</text>
		            <text class="features-content">{{ item.features }}</text>
		        </view>
		        
		        <!-- 额外信息 -->
		        <view class="additional-info" v-if="item.additional_info && item.additional_info !== '暂无额外信息'">
		            <text class="additional-title">详细信息:</text>
		            <text class="additional-content">{{ item.additional_info }}</text>
		        </view>
		        
		        <!-- 位置信息 -->
		        <view class="bbox-info">
		            位置坐标: [{{ Math.round(item.bbox[0]) }}, {{ Math.round(item.bbox[1]) }}, 
		            {{ Math.round(item.bbox[2]) }}, {{ Math.round(item.bbox[3]) }}]
		        </view>
		    </view>
		</view>
		
		<view class="no-results" v-else>
			<text class="no-results-text">未检测到物体</text>
		</view>
		
		<!-- 操作按钮 -->
		<view class="action-buttons">
			<button class="back-btn" @tap="goBack">返回首页</button>
			<button class="retry-btn" @tap="retryDetection">重新检测</button>
		</view>
	</view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const resultData = ref(null)
const imagePath = ref('')

onLoad((options) => {
	if (options.data) {
		try {
			resultData.value = JSON.parse(decodeURIComponent(options.data))
			console.log('=== 解析后的数据 ===')
			console.log('完整数据:', JSON.stringify(resultData.value, null, 2))
			if (resultData.value.detections && resultData.value.detections.length > 0) {
				const firstItem = resultData.value.detections[0]
				console.log('第一个检测物体:', firstItem)
				console.log('description原始值:', firstItem.description)
				console.log('features原始值:', firstItem.features)
				console.log('additional_info原始值:', firstItem.additional_info)
			}
		} catch (error) {
			console.error('解析数据错误:', error)
		}
	}
	if (options.imagePath) {
		imagePath.value = decodeURIComponent(options.imagePath)
	}
})

const goBack = () => {
	uni.navigateBack()
}

const retryDetection = () => {
	uni.navigateBack()
}
</script>

<style scoped>
.container {
	padding: 30rpx;
	min-height: 100vh;
	background: #f5f5f5;
}

.header {
	text-align: center;
	margin-bottom: 40rpx;
}

.title {
	display: block;
	font-size: 48rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 10rpx;
}

.subtitle {
	display: block;
	font-size: 28rpx;
	color: #666;
}

.image-section {
	background: white;
	border-radius: 20rpx;
	padding: 20rpx;
	margin-bottom: 30rpx;
	box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.1);
}

.preview-image {
	width: 100%;
	border-radius: 10rpx;
}

.results-section {
	margin-bottom: 40rpx;
}

.result-item {
	background: white;
	border-radius: 20rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.1);
}

.item-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20rpx;
}

.object-name {
	font-size: 36rpx;
	font-weight: bold;
	color: #007AFF;
}

.confidence {
	font-size: 28rpx;
	color: #FF9500;
	font-weight: 500;
}

.category-info {
    margin-bottom: 15rpx;
}

.category-label {
    font-size: 26rpx;
    color: #5856D6;
    background: #f0f0ff;
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-weight: 500;
}

.item-description {
	font-size: 28rpx;
	color: #333;
	line-height: 1.6;
	margin-bottom: 15rpx;
}

.features-info, .additional-info {
    margin-bottom: 15rpx;
}

.features-title, .additional-title {
    display: block;
    font-size: 26rpx;
    color: #333;
    font-weight: bold;
    margin-bottom: 5rpx;
}

.features-content, .additional-content {
    display: block;
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
}

.bbox-info {
	font-size: 24rpx;
	color: #666;
	background: #f8f8f8;
	padding: 15rpx;
	border-radius: 10rpx;
}

.no-results {
	text-align: center;
	padding: 100rpx 0;
}

.no-results-text {
	font-size: 32rpx;
	color: #999;
}

.action-buttons {
	display: flex;
	gap: 20rpx;
}

.back-btn, .retry-btn {
	flex: 1;
	height: 80rpx;
	border-radius: 15rpx;
	font-size: 32rpx;
	border: none;
}

.back-btn {
	background: #666;
	color: white;
}

.retry-btn {
	background: #007AFF;
	color: white;
}
</style>