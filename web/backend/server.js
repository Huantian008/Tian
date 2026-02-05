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
    (async () => {
        const { message } = req.body;

        // 验证请求数据
        if (!message) {
            return res.status(400).json({ error: '消息不能为空' });
        }

        const fallbackResponses = [
            '你好！我能帮你什么忙吗？',
            '这是一个很有趣的问题！',
            '我理解你的意思了。',
            '让我思考一下这个问题...',
            '谢谢你的提问！',
            '我是一个简单的AI助手，我的能力有限。',
            '这个问题很复杂，但我会尽力回答。',
            '我喜欢与你聊天！'
        ];

        function pickFallback() {
            return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
        }

        async function callGeminiText(promptText) {
            const apiKey = process.env.GEMINI_API_KEY;
            if (!apiKey) return null;

            const model = process.env.GEMINI_MODEL || 'gemini-1.5-flash';
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(apiKey)}`;

            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 20000);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contents: [
                            {
                                role: 'user',
                                parts: [{ text: String(promptText) }]
                            }
                        ],
                        generationConfig: {
                            temperature: 0.7,
                            maxOutputTokens: 256
                        }
                    }),
                    signal: controller.signal,
                });

                if (!response.ok) {
                    const errText = await response.text().catch(() => '');
                    throw new Error(`Gemini API 返回状态 ${response.status}${errText ? `: ${errText}` : ''}`);
                }

                const data = await response.json();
                const text = data?.candidates?.[0]?.content?.parts?.map(p => p?.text).filter(Boolean).join('') || '';
                return text.trim() || null;
            } finally {
                clearTimeout(timeout);
            }
        }

        try {
            const geminiText = await callGeminiText(message);
            if (geminiText) {
                return res.json({ response: geminiText });
            }

            // 未配置 GEMINI_API_KEY 时，回退到本地模拟响应
            return res.json({ response: pickFallback() });
        } catch (error) {
            console.error('AI聊天错误:', error);
            // Gemini 调用失败时也回退，保证前端可用
            return res.json({ response: pickFallback() });
        }
    })();
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
