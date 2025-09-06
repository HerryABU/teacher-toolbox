/**
 * 教师工具箱 - 工具函数库
 * 作者: AiPy
 * 版本: 2.0
 * 功能: 提供本地JSON文件读取等工具函数
 */

// 创建全局工具箱工具对象
window.ToolboxUtils = {
    // 配置选项
    config: {
        // 请求超时时间（毫秒）
        timeout: 10000,
        
        // 最大重试次数
        maxRetries: 3,
        
        // 重试延迟（毫秒）
        retryDelay: 1000
    },
    
    /**
     * 安全加载本地JSON配置文件
     * 支持非server环境下的文件读取
     * @param {string} path - 配置文件路径
     * @param {Object} options - 可选配置选项
     * @returns {Promise<Object|null>} 配置数据
     */
    async loadConfig(path, options = {}) {
        const config = { ...this.config, ...options };
        let lastError = null;
        
        // 尝试多次加载
        for (let attempt = 1; attempt <= config.maxRetries; attempt++) {
            try {
                // 优先使用fetch API
                if (this.isFetchSupported()) {
                    const result = await this.loadWithFetch(path, config.timeout);
                    if (result) return result;
                }
                
                // 备用方案：使用XMLHttpRequest
                const result = await this.loadWithXHR(path, config.timeout);
                if (result) return result;
                
                // 如果两种方法都失败，抛出错误
                throw new Error(`所有加载方法都失败`);
                
            } catch (error) {
                lastError = error;
                console.warn(`加载配置文件失败 (尝试 ${attempt}/${config.maxRetries}): ${path}`, error);
                
                // 如果不是最后一次尝试，等待后重试
                if (attempt < config.maxRetries) {
                    await this.delay(config.retryDelay * attempt);
                }
            }
        }
        
        // 所有尝试都失败
        console.error(`❌ 配置文件读取失败: ${path}`, lastError);
        return null;
    },
    
    /**
     * 使用fetch API加载JSON文件
     * @param {string} path - 文件路径
     * @param {number} timeout - 超时时间
     * @returns {Promise<Object|null>} 解析后的数据
     */
    async loadWithFetch(path, timeout) {
        try {
            // 创建AbortController用于超时控制
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            
            const response = await fetch(path, {
                signal: controller.signal,
                headers: {
                    'Accept': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
            
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error(`请求超时 (${timeout}ms)`);
            }
            throw error;
        }
    },
    
    /**
     * 使用XMLHttpRequest加载JSON文件
     * @param {string} path - 文件路径
     * @param {number} timeout - 超时时间
     * @returns {Promise<Object|null>} 解析后的数据
     */
    loadWithXHR(path, timeout) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            let timeoutId;
            
            // 设置超时
            const onTimeout = () => {
                xhr.abort();
                reject(new Error(`请求超时 (${timeout}ms)`));
            };
            
            timeoutId = setTimeout(onTimeout, timeout);
            
            // 配置请求
            xhr.open('GET', path, true);
            xhr.overrideMimeType('application/json');
            xhr.setRequestHeader('Accept', 'application/json');
            
            // 请求完成处理
            xhr.onreadystatechange = () => {
                if (xhr.readyState !== 4) return;
                
                clearTimeout(timeoutId);
                
                // 检查响应状态
                const isSuccess = (xhr.status === 200) || 
                                (xhr.status === 0 && xhr.responseText);
                
                if (!isSuccess) {
                    reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
                    return;
                }
                
                // 解析JSON数据
                try {
                    const data = JSON.parse(xhr.responseText);
                    resolve(data);
                } catch (parseError) {
                    reject(new Error(`JSON解析失败: ${parseError.message}`));
                }
            };
            
            // 网络错误处理
            xhr.onerror = () => {
                clearTimeout(timeoutId);
                reject(new Error('网络请求失败'));
            };
            
            // 发送请求
            xhr.send();
        });
    },
    
    /**
     * 检查当前环境是否支持fetch
     * @returns {boolean} 是否支持
     */
    isFetchSupported() {
        return typeof fetch !== 'undefined' && 
               typeof AbortController !== 'undefined' &&
               typeof Headers !== 'undefined';
    },
    
    /**
     * 延迟函数
     * @param {number} ms - 延迟毫秒数
     * @returns {Promise<void>}
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    
    /**
     * 获取相对路径
     * @param {string} basePath - 基础路径
     * @param {string} targetPath - 目标路径
     * @returns {string} 相对路径
     */
    getRelativePath(basePath, targetPath) {
        const baseParts = basePath.split('/').filter(part => part !== '');
        const targetParts = targetPath.split('/').filter(part => part !== '');
        
        // 移除共同的前缀
        while (baseParts.length && targetParts.length && 
               baseParts[0] === targetParts[0]) {
            baseParts.shift();
            targetParts.shift();
        }
        
        // 计算返回上级目录的数量
        const upCount = Math.max(0, baseParts.length - 1);
        const relativePath = '../'.repeat(upCount) + targetParts.join('/');
        
        return relativePath;
    },
    
    /**
     * 深度合并对象
     * @param {Object} target - 目标对象
     * @param {...Object} sources - 源对象
     * @returns {Object} 合并后的对象
     */
    deepMerge(target, ...sources) {
        if (!sources.length) return target;
        const source = sources.shift();
        
        if (this.isObject(target) && this.isObject(source)) {
            for (const key in source) {
                if (this.isObject(source[key])) {
                    if (!target[key]) Object.assign(target, { [key]: {} });
                    this.deepMerge(target[key], source[key]);
                } else {
                    Object.assign(target, { [key]: source[key] });
                }
            }
        }
        
        return this.deepMerge(target, ...sources);
    },
    
    /**
     * 检查是否为对象
     * @param {*} item - 检查项
     * @returns {boolean} 是否为对象
     */
    isObject(item) {
        return item && typeof item === 'object' && !Array.isArray(item);
    },
    
    /**
     * 格式化文件大小
     * @param {number} bytes - 字节数
     * @returns {string} 格式化后的大小
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
};

// 初始化调试信息
console.log('📚 ToolboxUtils 工具库已加载');
console.log('🔧 支持的功能:');
console.log('  - 本地JSON文件读取');
console.log('  - 超时和重试机制');
console.log('  - 多种加载方式兼容');
console.log('  - 路径处理工具');
console.log('  - 对象深度合并');
console.log('  - 文件大小格式化');
