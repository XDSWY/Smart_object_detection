<template>
    <view class="container">
        <!-- 头部 -->
        <view class="header">
            <text class="title">关于我们</text>
            <text class="subtitle">About Our App</text>
        </view>
        
        <!-- 应用信息 -->
        <view class="app-info">
            <image class="app-logo" src="/static/images/logo.png" mode="aspectFit"></image>
            <text class="app-name">智能图像检测</text>
            <text class="app-version">版本 1.0.0</text>
        </view>
        
        <!-- 功能特点 -->
        <view class="features">
            <view class="feature-item">
                <text class="feature-icon">🔍</text>
                <text class="feature-title">智能检测</text>
                <text class="feature-desc">基于YOLOv8深度学习模型</text>
            </view>
            
            <view class="feature-item">
                <text class="feature-icon">🚀</text>
                <text class="feature-title">快速识别</text>
                <text class="feature-desc">实时物体检测与分类</text>
            </view>
            
            <view class="feature-item">
                <text class="feature-icon">📱</text>
                <text class="feature-title">多端支持</text>
                <text class="feature-desc">基于Uni-App跨端框架</text>
            </view>
        </view>
        
        <!-- 技术栈 -->
        <view class="tech-stack">
            <text class="section-title">技术栈</text>
            <view class="tech-list">
                <text class="tech-item">• 前端: Uni-App + Vue3</text>
                <text class="tech-item">• 后端: Flask + Python</text>
                <text class="tech-item">• 算法: YOLOv8 模型</text>
                <text class="tech-item">• 部署: 本地开发环境</text>
            </view>
        </view>
        
        <!-- 返回按钮 -->
        <view class="footer">
            <button class="back-btn" @tap="goBack">返回首页</button>
        </view>
    </view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app'

// 页面加载时打印日志
onLoad((options) => {
    console.log('关于页面加载成功', options)
})

const goBack = () => {
    uni.navigateBack({
        success: () => {
            console.log('返回首页成功')
        },
        fail: (error) => {
            console.error('返回失败:', error)
            // 如果返回失败，重定向到首页
            uni.redirectTo({
                url: '/pages/index/index'
            })
        }
    })
}
</script>

<style scoped>
.container {
    padding: 40rpx;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
    text-align: center;
    margin-bottom: 60rpx;
    margin-top: 40rpx;
}

.title {
    display: block;
    font-size: 48rpx;
    font-weight: bold;
    color: white;
    margin-bottom: 10rpx;
}

.subtitle {
    display: block;
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.8);
}

.app-info {
    text-align: center;
    margin-bottom: 60rpx;
}

.app-logo {
    width: 120rpx;
    height: 120rpx;
    border-radius: 24rpx;
    background: white;
    padding: 20rpx;
    margin-bottom: 20rpx;
}

.app-name {
    display: block;
    font-size: 36rpx;
    color: white;
    font-weight: bold;
    margin-bottom: 10rpx;
}

.app-version {
    display: block;
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.8);
}

.features {
    margin-bottom: 50rpx;
}

.feature-item {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    text-align: center;
}

.feature-icon {
    display: block;
    font-size: 60rpx;
    margin-bottom: 15rpx;
}

.feature-title {
    display: block;
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 10rpx;
}

.feature-desc {
    display: block;
    font-size: 26rpx;
    color: #666;
}

.tech-stack {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 40rpx;
}

.section-title {
    display: block;
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
}

.tech-list {
    display: flex;
    flex-direction: column;
    gap: 15rpx;
}

.tech-item {
    font-size: 28rpx;
    color: #666;
}

.footer {
    margin-top: 40rpx;
}

.back-btn {
    width: 100%;
    height: 80rpx;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    border-radius: 15rpx;
    font-size: 32rpx;
    backdrop-filter: blur(10px);
}

.back-btn:active {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0.98);
}
</style>