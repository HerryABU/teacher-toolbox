

# 🛠️ 教师工具箱 (Teacher Toolbox)

> **一个正在构建中的开源教育工具平台**
>
> 🔗 **项目主页**: [https://gitee.com/feng-minamata-hao/teacher-toolbox](https://gitee.com/feng-minamata-hao/teacher-toolbox)

## 🌟 项目简介

`teacher-toolbox` 是一个旨在为教育工作者提供便捷工具的开源项目。它采用模块化设计，将各类教学辅助功能整合于一个统一的框架内。

本项目目前处于 **积极开发和构建阶段**。我们已成功搭建了核心架构，并集成了多个工具模块。我们深知，一个真正有价值的平台离不开广大教育同仁的智慧与贡献，因此，我们诚挚地邀请您加入我们的社区，共同完善这个项目！

## 🧱 核心架构：双级目录与多 JSON 驱动

本项目的后端数据与前端路由完全由 **双级目录结构** 和 **多 JSON 配置文件** 驱动，实现了高度的灵活性和可扩展性。

### 📁 目录结构

项目的工具模块采用清晰的双级目录设计：

```
tools/
├── categories/                 # 第一级：功能大类
│   ├── enrollment_management/  # 例如：入学管理
│   │   ├── config.json         # 大类配置文件
│   │   └── tools/              # 包含该大类下的所有具体工具
│   │       ├── smart_class_division/
│   │       ├── seat_arrangement/
│   │       └── student_id_generator/
│   ├── classroom_interaction/  # 例如：课堂互动
│   │   ├── config.json
│   │   └── tools/
│   │       ├── random_student_selector/
│   │       └── classroom_scoreboard/
│   └── ...                     # 更多大类
├── config.json                 # 全局配置文件
└── index.html                  # 工具大类导航页
```

### 📄 JSON 配置驱动

系统通过读取多层级的 `config.json` 文件来动态生成内容：
*   **全局配置** (`tools/config.json`): 定义所有功能大类。
*   **大类配置** (`tools/categories/*/config.json`): 定义该大类下的所有具体工具。
*   **工具实现**: 每个工具拥有自己的 `index.html` 作为独立页面。

这种设计使得**新增一个工具或大类变得极其简单**：只需在对应目录下创建文件夹并编写 `config.json` 和页面文件即可，无需修改核心代码。

## 🙏 特别鸣谢 (Special Thanks)

我们非常感谢所有为本项目提供支持和帮助的个人与社区。在本项目的 `announcement` 分类下，我们设立了一个“特别鸣谢”模块。

*   **开发者可以自行添加**: 项目的维护者或贡献者可以编辑 `tools/categories/announcement/tools/authorization/thanks-data.json` 文件，将您希望感谢的个人或组织信息添加进去。
*   这个模块旨在记录和展示项目发展过程中的支持与贡献。

## 🚧 项目状态与社区支持

*   **当前状态**: 项目正在积极构建中。核心框架和目录结构已稳定，目前已有 **5 个及以上**的工具模块被集成或正在开发。
*   **社区支持**: 这是一个由社区驱动的开源项目。我们迫切需要您的帮助：
    *   **架构优化**: 您对当前的双 JSON 驱动架构有何改进建议？
    *   **新模块开发**: 您希望增加哪些新的功能大类或工具？
    *   **贡献代码**: 如果您有编程技能，欢迎提交 Pull Request，为架构或新工具贡献力量。
    *   **测试与反馈**: 帮助我们测试现有结构的稳定性和易用性。

## 📦 快速开始

本项目使用了现代 Web 技术（如 `fetch` API），**无法通过直接双击 `index.html` 文件的方式运行**（会因浏览器的跨域安全策略而失败）。

**必须在本地启动一个 HTTP 服务器**来访问项目。您可以使用任何您熟悉的服务器工具，例如：

*   **Node.js 的 `http-server`**:
    ```bash
    npm install -g http-server
    http-server -p 8080
    ```

*   **Python 3 的内置服务器**:
    ```bash
    python -m http.server 8080
    ```

*   **Python 2 的内置服务器**:
    ```bash
    python -m SimpleHTTPServer 8080
    ```

*   或其他任何能提供静态文件服务的 Web 服务器 (如 Nginx, Apache 等)。

启动服务器后，在浏览器中访问 `http://localhost:8080` (或您指定的端口) 即可使用。

> **注意**: 当前版本的上传功能尚未完全开放，我们正在努力构建更安全、更便捷的文件上传通道。

## 📜 版权与许可

本项目遵循 **GPL-3.0** 开源协议。这意味着您可以自由地使用、修改和分发本软件，但任何基于本项目的衍生作品也必须以相同的 GPL-3.0 协议开源。

---

**让我们携手共建一个更智能、更高效的教师工作环境！**

---
**© 2024 开源教师工具箱，欢迎社区提供。**