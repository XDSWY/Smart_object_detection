const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          '^/api': ''  // 将 /api 替换为空字符串
        },
        logLevel: 'debug'
      }
    },
    host: 'localhost',
    port: 8080,
    open: true
  }
})