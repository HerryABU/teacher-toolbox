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


@app.route('/tools/<path:filename>')
def serve_tool_files(filename):
    tools_dir = os.path.join(app.root_path, '..', 'tools')
    return send_from_directory(tools_dir, filename)

    
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

# API端点用于添加/删除功能
@app.route('/api/tools', methods=['POST'])
def add_tool():
    """添加新工具或分类"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    # 获取操作类型
    operation = data.get('operation', 'tool')
    
    if operation == 'category':
        # 添加新分类
        category_id = data.get('category_id')
        category_name = data.get('category_name')
        category_icon = data.get('category_icon', 'DocumentAdd')
        
        if not category_id or not category_name:
            return jsonify({'error': '缺少分类ID或名称'}), 400
        
        # 加载主配置
        config_path = BASE_PATH / 'tools' / 'config.json'
        main_config = load_json_file(config_path)
        
        if not main_config:
            main_config = {"categories": []}
        
        # 检查分类是否已存在
        for cat in main_config['categories']:
            if cat['id'] == category_id:
                return jsonify({'error': '分类已存在'}), 400
        
        # 添加新分类
        new_category = {
            "id": category_id,
            "name": category_name,
            "icon": category_icon,
            "path": f"/tools/categories/{category_id}"
        }
        
        main_config['categories'].append(new_category)
        
        # 保存主配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(main_config, f, ensure_ascii=False, indent=2)
        
        # 创建分类目录和配置文件
        category_path = BASE_PATH / 'tools' / 'categories' / category_id
        category_path.mkdir(parents=True, exist_ok=True)
        
        # 创建分类配置文件
        category_config_path = category_path / 'config.json'
        with open(category_config_path, 'w', encoding='utf-8') as f:
            json.dump({"tools": []}, f, ensure_ascii=False, indent=2)
        
        return jsonify({'message': '分类添加成功', 'category': new_category}), 200
    
    elif operation == 'tool':
        # 添加新工具
        category_id = data.get('category_id')
        tool_id = data.get('tool_id')
        tool_name = data.get('tool_name')
        tool_description = data.get('tool_description', '')
        tool_icon = data.get('tool_icon', 'Aim')
        
        if not category_id or not tool_id or not tool_name:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 加载分类配置
        category_path = BASE_PATH / 'tools' / 'categories' / category_id
        config_path = category_path / 'config.json'
        category_config = load_json_file(config_path)
        
        if not category_config:
            category_config = {"tools": []}
        
        # 检查工具是否已存在
        for tool in category_config['tools']:
            if tool['id'] == tool_id:
                return jsonify({'error': '工具已存在'}), 400
        
        # 添加新工具
        new_tool = {
            "id": tool_id,
            "name": tool_name,
            "description": tool_description,
            "icon": tool_icon,
            "path": f"./tools/{tool_id}/index.html"
        }
        
        category_config['tools'].append(new_tool)
        
        # 保存分类配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(category_config, f, ensure_ascii=False, indent=2)
        
        # 创建工具目录和文件
        tool_path = category_path / 'tools' / tool_id
        tool_path.mkdir(parents=True, exist_ok=True)
        
        # 创建默认的index.html文件
        default_html_path = tool_path / 'index.html'
        with open(default_html_path, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tool_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #303133;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{tool_name}</h1>
        <p>{tool_description}</p>
        <p>这是一个新创建的工具页面，您可以在此处添加具体功能。</p>
    </div>
</body>
</html>""")
        
        return jsonify({'message': '工具添加成功', 'tool': new_tool}), 200
    
    else:
        return jsonify({'error': '未知操作类型'}), 400

@app.route('/api/tools/<category_id>/<tool_id>', methods=['DELETE'])
def delete_tool(category_id, tool_id):
    """删除工具"""
    # 加载分类配置
    category_path = BASE_PATH / 'tools' / 'categories' / category_id
    config_path = category_path / 'config.json'
    category_config = load_json_file(config_path)
    
    if not category_config or 'tools' not in category_config:
        return jsonify({'error': '分类配置不存在'}), 404
    
    # 过滤掉要删除的工具
    original_count = len(category_config['tools'])
    category_config['tools'] = [tool for tool in category_config['tools'] if tool['id'] != tool_id]
    
    if len(category_config['tools']) == original_count:
        return jsonify({'error': '工具不存在'}), 404
    
    # 保存分类配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(category_config, f, ensure_ascii=False, indent=2)
    
    # 删除工具目录（如果存在）
    tool_path = category_path / 'tools' / tool_id
    import shutil
    if tool_path.exists():
        shutil.rmtree(tool_path)
    
    return jsonify({'message': '工具删除成功'}), 200

@app.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """删除分类"""
    # 加载主配置
    config_path = BASE_PATH / 'tools' / 'config.json'
    main_config = load_json_file(config_path)
    
    if not main_config or 'categories' not in main_config:
        return jsonify({'error': '主配置不存在'}), 404
    
    # 过滤掉要删除的分类
    original_count = len(main_config['categories'])
    main_config['categories'] = [cat for cat in main_config['categories'] if cat['id'] != category_id]
    
    if len(main_config['categories']) == original_count:
        return jsonify({'error': '分类不存在'}), 404
    
    # 保存主配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(main_config, f, ensure_ascii=False, indent=2)
    
    # 删除分类目录（如果存在）
    category_path = BASE_PATH / 'tools' / 'categories' / category_id
    import shutil
    if category_path.exists():
        shutil.rmtree(category_path)
    
    return jsonify({'message': '分类删除成功'}), 200

# API端点用于处理班级Excel上传
@app.route('/api/upload/class', methods=['POST'])
def upload_class_excel():
    """上传班级Excel文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and file.filename.lower().endswith(('.xlsx', '.xls')):
        import pandas as pd
        import io
        
        try:
            # 读取Excel文件
            file_content = file.read()
            df = pd.read_excel(io.BytesIO(file_content))
            
            # 获取基本的班级信息（假设前几列是基本信息）
            # 这里可以根据实际Excel格式进行调整
            class_data = {
                'columns': df.columns.tolist(),
                'rows': df.to_dict('records'),
                'total_rows': len(df),
                'file_name': file.filename
            }
            
            # 可以在这里添加数据验证和处理逻辑
            # 例如检查必需字段、格式验证等
            
            return jsonify({
                'message': '文件上传成功',
                'data': class_data
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'处理Excel文件时出错: {str(e)}'}), 500
    else:
        return jsonify({'error': '不支持的文件格式，请上传Excel文件(.xlsx或.xls)'}), 400

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