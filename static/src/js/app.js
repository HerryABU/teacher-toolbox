// 教师工具箱 - Vue应用
// 作者: AiPy
// 版本: 2.0

// 确保ToolboxUtils已加载
if (typeof window.ToolboxUtils === 'undefined') {
    console.error('ToolboxUtils未加载，请检查utils.js');
}

// 创建Vue应用
const { createApp } = Vue;

// 应用配置
const appConfig = {
    // 加载超时时间（毫秒）
    loadTimeout: 10000,
    
    // 重试次数
    retryCount: 3,
    
    // 默认展开状态
    defaultExpanded: true
};

// 创建Vue应用实例
const app = createApp({
    data() {
        return {
            // 分类数据
            categories: [],
            
            // 加载状态
            loading: true,
            
            // 错误信息
            error: null,
            
            // 当前选中的分类
            selectedCategory: null,
            
            // 侧边栏展开状态
            sidebarOpen: false
        };
    },
    
    // 组件挂载后执行
    async mounted() {
        await this.loadCategoriesWithTools();
    },
    
    methods: {
        /**
         * 加载分类和工具数据
         */
        async loadCategoriesWithTools() {
            try {
                this.loading = true;
                this.error = null;
                
                // 加载主配置文件
                const categoryData = await this.safeLoadConfig('tools/config.json');
                if (!categoryData || !categoryData.categories) {
                    throw new Error('配置文件格式错误');
                }
                
                // 初始化分类数据
                this.categories = categoryData.categories.map(category => ({
                    ...category,
                    expanded: appConfig.defaultExpanded,
                    tools: []
                }));
                
                // 并行加载所有分类的工具数据
                const toolLoadPromises = this.categories.map(async category => {
                    try {
                        const categoryPath = category.path.replace('/tools/categories', '');
                        const toolData = await this.safeLoadConfig(`tools/categories${categoryPath}/config.json`);
                        
                        if (toolData && Array.isArray(toolData.tools)) {
                            category.tools = toolData.tools;
                        }
                    } catch (toolError) {
                        console.warn(`加载分类 ${category.name} 的工具数据失败:`, toolError);
                    }
                });
                
                // 等待所有工具数据加载完成
                await Promise.all(toolLoadPromises);
                
                console.log('✅ 成功加载所有分类和工具数据:', this.categories);
                
            } catch (error) {
                console.error('❌ 加载分类数据失败:', error);
                this.error = `无法加载工具分类数据: ${error.message}`;
            } finally {
                this.loading = false;
            }
        },
        
        /**
         * 安全加载配置文件
         * @param {string} path - 配置文件路径
         * @returns {Promise<Object|null>} 配置数据
         */
        async safeLoadConfig(path) {
            try {
                // 尝试使用ToolboxUtils
                if (window.ToolboxUtils && window.ToolboxUtils.loadConfig) {
                    return await window.ToolboxUtils.loadConfig(path);
                }
                
                // 回退到fetch
                if (window.fetch) {
                    const response = await fetch(path);
                    if (response.ok) {
                        return await response.json();
                    }
                }
                
                throw new Error(`无法加载 ${path}`);
                
            } catch (error) {
                console.error(`❌ 配置文件读取失败 (${path}):`, error);
                return null;
            }
        },
        
        /**
         * 切换分类的展开/折叠状态
         * @param {Object} category - 分类对象
         */
        toggleCategory(category) {
            // 切换展开状态
            category.expanded = !category.expanded;
            
            // 移动端关闭侧边栏
            if (window.innerWidth <= 768) {
                this.sidebarOpen = false;
            }
        },
        
        /**
         * 选择分类
         * @param {Object} category - 分类对象
         */
        selectCategory(category) {
            this.selectedCategory = category.id;
            
            // 移动端关闭侧边栏
            if (window.innerWidth <= 768) {
                this.sidebarOpen = false;
            }
        },
        
        /**
         * 切换侧边栏状态
         */
        toggleSidebar() {
            this.sidebarOpen = !this.sidebarOpen;
        },
        
        /**
         * 获取图标
         * @param {string} iconName - 图标名称
         * @returns {string} 图标字符
         */
        getIcon(iconName) {
            const icons = {
                'DocumentAdd': '📄',
                'ChatLineSquare': '💬',
                'EditPen': '✏️',
                'Calendar': '📅',
                'Medal': '🏆',
                'Aim': '🎯',
                'Grid': '📊',
                'Tickets': '🎫',
                'UserFilled': '👤',
                'Dice': '🎲',
                'Check': '✅',
                'Trophy': '🏆',
                'DataAnalysis': '📈',
                'TrendCharts': '📉',
                'Collection': '📚',
                'Bell': '🔔',
                'Message': '💬',
                'FirstAid': '🏥',
                'Box': '📦',
                'List': '📋'
            };
            return icons[iconName] || '🔧';
        }
    }
});

// 挂载应用
app.mount('#app');

// 调试信息
console.log('✨ 教师工具箱Vue应用已成功挂载');
console.log('📦 应用配置:', appConfig);
