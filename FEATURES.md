# 教师工具箱 - 新增功能说明

## 1. 模块添加/删除功能

### 添加模块 (add.html)
- 用户可以通过界面添加新的工具分类和工具
- 支持选择现有分类或创建新分类
- 支持添加新工具到现有分类或新创建的分类
- 所有操作通过后端API实现，直接修改JSON配置文件和创建相应的目录结构

### 删除模块 (del.html)
- 用户可以通过界面删除现有的工具分类和工具
- 提供确认对话框以防止误删
- 所有操作通过后端API实现，直接修改JSON配置文件和删除相应的目录结构

## 2. 班级信息上传功能 (class_upload.html)

### 功能特点
- 支持拖拽上传Excel文件（.xlsx和.xls格式）
- 文件大小限制为10MB
- 上传后显示数据预览，包括前10条记录
- 显示文件统计信息（总记录数、列数等）

### 后端处理
- 使用pandas库处理Excel文件
- 解析Excel数据并返回JSON格式的结果
- 验证文件格式和大小

## 3. API端点

### 添加/删除功能API
- `POST /api/tools` - 添加新分类或工具
- `DELETE /api/tools/<category_id>/<tool_id>` - 删除工具
- `DELETE /api/categories/<category_id>` - 删除分类

### 上传功能API
- `POST /api/upload/class` - 上传班级Excel文件

### 配置获取API
- `GET /api/config/tools` - 获取工具分类配置
- `GET /api/config/tools/categories/<category_id>` - 获取特定分类的工具配置

## 4. 目录结构

```
/workspace/
├── add.html              # 添加模块页面
├── del.html              # 删除模块页面
├── class_upload.html     # 班级上传页面
├── app/
│   └── main.py           # Flask后端实现
├── tools/
│   ├── config.json       # 主配置文件
│   └── categories/       # 分类目录
└── requirements.txt      # 依赖包
```

## 5. 依赖包

新增了以下Python包：
- pandas - 用于处理Excel文件
- openpyxl - Excel文件读写支持

## 6. 使用说明

1. 启动服务器：`python run.py`
2. 访问主页：http://localhost:5000
3. 使用"添加项目"和"删除项目"按钮管理工具
4. 使用"上传班级名单"功能上传Excel文件