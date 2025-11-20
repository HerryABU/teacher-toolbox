"""
Flask应用主入口
重构教师工具箱，使用Python Flask作为主框架
保持原有的JSON目录格式不变，仅重构外部HTML框架
"""
from flask import Flask, render_template, jsonify, send_from_directory, request
import json
import os
from pathlib import Path

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# 定义基础路径
BASE_PATH = Path(__file__).parent.parent

def load_json_file(filepath):
    """加载JSON配置文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件未找到: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"JSON解析错误: {filepath}")
        return None

@app.route('/')
def index():
    """主页 - 显示所有分类"""
    config_path = BASE_PATH / 'tools' / 'config.json'
    data = load_json_file(config_path)
    
    if data and 'categories' in data:
        categories = data['categories']
        # 为每个分类加载其工具列表
        for category in categories:
            category_path = BASE_PATH / category['path'].replace('/tools', 'tools', 1).lstrip('/')
            category_config_path = category_path / 'config.json'
            category_data = load_json_file(category_config_path)
            if category_data and 'tools' in category_data:
                category['tools'] = category_data['tools']
            else:
                category['tools'] = []
        return render_template('index.html', categories=categories)
    else:
        return render_template('index.html', categories=[])

@app.route('/tools/')
def tools_index():
    """工具分类页面"""
    config_path = BASE_PATH / 'tools' / 'config.json'
    data = load_json_file(config_path)
    
    if data and 'categories' in data:
        return render_template('tools/index.html', categories=data['categories'])
    else:
        return render_template('tools/index.html', categories=[])

@app.route('/tools/categories/<category_id>/')
def category_tools(category_id):
    """特定分类的工具列表页面"""
    # 根据category_id找到对应的目录
    category_path = BASE_PATH / 'tools' / 'categories' / category_id
    config_path = category_path / 'config.json'
    
    data = load_json_file(config_path)
    
    if data and 'tools' in data:
        # 获取分类信息
        main_config_path = BASE_PATH / 'tools' / 'config.json'
        main_data = load_json_file(main_config_path)
        
        category_info = None
        if main_data and 'categories' in main_data:
            for cat in main_data['categories']:
                if cat['id'] == category_id:
                    category_info = cat
                    break
        
        return render_template('tools/categories/index.html', 
                             tools=data['tools'], 
                             category=category_info)
    else:
        return render_template('tools/categories/index.html', tools=[], category=None)

# 静态文件路由 - 保持原有路径结构
@app.route('/src/<path:filename>')
def src_static(filename):
    return send_from_directory(BASE_PATH / 'src', filename)

@app.route('/vendor/<path:filename>')
def vendor_static(filename):
    return send_from_directory(BASE_PATH / 'vendor', filename)

@app.route('/tools/src/<path:filename>')
def tools_src_static(filename):
    return send_from_directory(BASE_PATH / 'tools' / 'src', filename)

@app.route('/tools/vendor/<path:filename>')
def tools_vendor_static(filename):
    return send_from_directory(BASE_PATH / 'tools' / 'vendor', filename)

@app.route('/tools/categories/<category_id>/src/<path:filename>')
def category_src_static(category_id, filename):
    category_path = BASE_PATH / 'tools' / 'categories' / category_id
    return send_from_directory(category_path / 'src', filename)

@app.route('/tools/categories/<category_id>/vendor/<path:filename>')
def category_vendor_static(category_id, filename):
    category_path = BASE_PATH / 'tools' / 'categories' / category_id
    return send_from_directory(category_path / 'vendor', filename)

# API端点用于获取JSON数据
@app.route('/api/config/tools')
def api_tools_config():
    """获取工具分类配置"""
    config_path = BASE_PATH / 'tools' / 'config.json'
    data = load_json_file(config_path)
    return jsonify(data if data else {})

@app.route('/api/config/tools/categories/<category_id>')
def api_category_config(category_id):
    """获取特定分类的工具配置"""
    category_path = BASE_PATH / 'tools' / 'categories' / category_id
    config_path = category_path / 'config.json'
    data = load_json_file(config_path)
    return jsonify(data if data else {})

# 保持原有HTML页面的路由（内部HTML工具页面）
@app.route('/tools/categories/<category_id>/tools/<tool_id>/')
def tool_page(category_id, tool_id):
    """工具页面 - 直接返回原始HTML文件"""
    tool_path = BASE_PATH / 'tools' / 'categories' / category_id / 'tools' / tool_id / 'index.html'
    if tool_path.exists():
        with open(tool_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        return "工具页面不存在", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)