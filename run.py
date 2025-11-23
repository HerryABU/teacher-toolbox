#!/usr/bin/env python3
"""
教师工具箱 - Python Flask应用启动脚本
此脚本用于启动重构后的Python Flask应用
保持原有的JSON目录格式不变，仅重构外部HTML框架
"""

from app.main import app

if __name__ == '__main__':
    print("🚀 启动教师工具箱 Flask 应用...")
    print("🌐 访问地址: http://localhost:5000")
    print("🔧 调试模式: 已启用")
    print("🛑 按 Ctrl+C 停止服务器")
    app.run(debug=True, host='0.0.0.0', port=5000)