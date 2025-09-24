// 后端API服务器
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

// 创建Express应用
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors()); // 允许跨域请求
app.use(bodyParser.json()); // 解析JSON请求体
app.use(express.static(path.join(__dirname))); // 提供静态文件

// 存储消息的文件路径
const messagesFilePath = path.join(__dirname, 'messages.json');

// 确保messages.json文件存在
if (!fs.existsSync(messagesFilePath)) {
    fs.writeFileSync(messagesFilePath, JSON.stringify([]), 'utf8');
}

// 主页路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// test页面路由
app.get('/test', (req, res) => {
    res.sendFile(path.join(__dirname, 'index-new.html'));
});

// API路由

// 获取所有消息
app.get('/api/messages', (req, res) => {
    try {
        const messages = JSON.parse(fs.readFileSync(messagesFilePath, 'utf8'));
        res.json(messages);
    } catch (error) {
        console.error('读取消息失败:', error);
        res.status(500).json({ error: '读取消息失败' });
    }
});

// 提交新消息
app.post('/api/messages', (req, res) => {
    try {
        const { name, email, message } = req.body;
        
        // 验证请求数据
        if (!name || !email || !message) {
            return res.status(400).json({ error: '所有字段都是必填的' });
        }
        
        // 读取现有消息
        const messages = JSON.parse(fs.readFileSync(messagesFilePath, 'utf8'));
        
        // 添加新消息
        const newMessage = {
            id: Date.now(), // 使用时间戳作为ID
            name,
            email,
            message,
            timestamp: new Date().toISOString()
        };
        
        messages.push(newMessage);
        
        // 保存更新后的消息
        fs.writeFileSync(messagesFilePath, JSON.stringify(messages, null, 2), 'utf8');
        
        res.status(201).json(newMessage);
    } catch (error) {
        console.error('保存消息失败:', error);
        res.status(500).json({ error: '保存消息失败' });
    }
});

// AI聊天API模拟
app.post('/api/chat', (req, res) => {
    try {
        const { message } = req.body;
        
        // 验证请求数据
        if (!message) {
            return res.status(400).json({ error: '消息不能为空' });
        }
        
        // 模拟AI响应
        const responses = [
            '你好！我能帮你什么忙吗？',
            '这是一个很有趣的问题！',
            '我理解你的意思了。',
            '让我思考一下这个问题...',
            '谢谢你的提问！',
            '我是一个简单的AI助手，我的能力有限。',
            '这个问题很复杂，但我会尽力回答。',
            '我喜欢与你聊天！'
        ];
        
        // 随机选择一个响应
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        
        // 延迟响应，模拟AI思考时间
        setTimeout(() => {
            res.json({ response: randomResponse });
        }, 1000);
        
    } catch (error) {
        console.error('AI聊天错误:', error);
        res.status(500).json({ error: '处理聊天请求失败' });
    }
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
});

// 在文件末尾添加
process.on('uncaughtException', (err) => {
    console.error('未捕获的异常:', err);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('未处理的Promise拒绝:', reason);
    process.exit(1);
});

// 优雅关闭
process.on('SIGTERM', () => {
    console.log('收到SIGTERM信号，正在关闭服务器...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('收到SIGINT信号，正在关闭服务器...');
    process.exit(0);
});