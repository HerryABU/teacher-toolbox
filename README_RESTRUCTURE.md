# 教师工具箱 - Python Flask重构说明

## 重构概述
本项目已从纯HTML/JavaScript架构重构为Python Flask Web应用，但保持了原有的JSON目录格式和内部HTML工具页面不变。

## 项目结构变化

### 旧架构
```
/workspace/
├── index.html          # 静态HTML页面
├── tools/
│   ├── config.json     # JSON配置
│   ├── index.html      # 静态HTML页面
│   └── categories/
│       └── [分类ID]/
│           ├── config.json
│           ├── index.html
│           └── tools/
│               └── [工具ID]/
│                   └── index.html
```

### 新架构
```
/workspace/
├── app/
│   ├── __init__.py     # Flask应用模块
│   └── main.py         # Flask主应用入口
├── templates/          # Jinja2模板目录
│   ├── index.html      # 主页模板
│   └── tools/
│       ├── index.html  # 工具分类模板
│       └── categories/
│           └── index.html  # 分类工具模板
├── static/             # 静态文件目录（符号链接到原目录）
├── run.py              # 启动脚本
├── requirements.txt    # Python依赖
└── [原有文件保持不变]
```

## 重构内容

### 1. Python Flask框架
- 使用Flask作为主框架
- 使用Jinja2模板引擎
- 实现了路由系统，将原有的静态HTML页面转换为动态模板

### 2. 保持不变的部分
- ✅ 所有JSON配置文件格式和位置保持不变
- ✅ 所有内部HTML工具页面保持不变
- ✅ 静态资源文件（CSS、JS、图片等）保持不变
- ✅ 目录结构保持不变

### 3. 重构的部分
- ❌ 主页框架（index.html）转换为Flask模板
- ❌ 工具分类页面转换为Flask模板
- ❌ 分类工具列表页面转换为Flask模板

## 运行方式

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动应用
```bash
python run.py
```

应用将在 `http://localhost:5000` 启动

## 路由映射

| 原路径 | 新路径 | 说明 |
|--------|--------|------|
| `/` | `/` | 主页 |
| `/tools/` | `/tools/` | 工具分类页 |
| `/tools/categories/{category_id}/` | `/tools/categories/{category_id}/` | 分类工具页 |
| `/tools/categories/{category_id}/tools/{tool_id}/` | `/tools/categories/{category_id}/tools/{tool_id}/` | 工具页（原始HTML） |

## 技术栈

- **后端**: Python Flask
- **模板引擎**: Jinja2
- **前端**: 原有的Vue.js、HTML、CSS、JavaScript
- **数据格式**: 原有的JSON配置文件

## 优势

1. **动态内容**: 模板系统允许动态渲染内容
2. **易于维护**: Python后端便于扩展和维护
3. **向后兼容**: 保持原有JSON格式和工具页面不变
4. **渐进式重构**: 可逐步将更多功能迁移到Python后端