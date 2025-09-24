// 二次元自我介绍网站脚本

// QQ链接处理函数
function openQQ() {
    // 检测设备类型
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        // 移动端：直接打开腾讯官方QQ链接
        window.open('https://qm.qq.com/q/uAfighnzP2', '_blank');
    } else {
        // PC端：显示QQ弹窗
        showQQModal();
    }
}

// 游戏角色展开/收起功能
function toggleCharacters(button) {
    const characterList = button.parentElement.nextElementSibling;
    const isExpanded = button.classList.contains('expanded');
    
    if (isExpanded) {
        // 收起
        characterList.classList.remove('show');
        button.classList.remove('expanded');
        setTimeout(() => {
            characterList.style.display = 'none';
        }, 400);
    } else {
        // 展开
        characterList.style.display = 'grid';
        button.classList.add('expanded');
        setTimeout(() => {
            characterList.classList.add('show');
        }, 10);
    }
}

// 邮箱弹窗功能
function showEmailModal() {
    const modal = document.getElementById('emailModal');
    modal.style.display = 'flex';
    // 使用setTimeout确保display属性生效后再添加show类
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

function closeEmailModal() {
    const modal = document.getElementById('emailModal');
    modal.classList.remove('show');
    // 等待动画完成后隐藏元素
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// 复制邮箱功能
function copyEmail() {
    const email = 'huantian008@outlook.com';
    const button = document.querySelector('.copy-email-btn');
    
    // 使用现代的Clipboard API
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(email).then(() => {
            showCopySuccess(button);
        }).catch(() => {
            fallbackCopyTextToClipboard(email, button);
        });
    } else {
        // 降级方案
        fallbackCopyTextToClipboard(email, button);
    }
}

// 降级复制方案
function fallbackCopyTextToClipboard(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(button);
    } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制邮箱地址：' + text);
    }
    
    document.body.removeChild(textArea);
}

// 显示复制成功效果
function showCopySuccess(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="ri-check-line"></i>已复制！';
    button.classList.add('copy-success');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('copy-success');
    }, 2000);
}

// QQ弹窗功能
function showQQModal() {
    const modal = document.getElementById('qqModal');
    modal.style.display = 'flex';
    // 使用setTimeout确保display属性生效后再添加show类
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

function closeQQModal() {
    const modal = document.getElementById('qqModal');
    modal.classList.remove('show');
    // 等待动画完成后隐藏元素
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// 手机访问QQ链接
function openQQMobile() {
    window.open('https://qm.qq.com/q/uAfighnzP2', '_blank');
    closeQQModal();
}

// 复制QQ号功能
function copyQQNumber() {
    const qqNumber = '787603021';
    const button = document.querySelector('.copy-qq-btn');
    
    // 使用现代的Clipboard API
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(qqNumber).then(() => {
            showCopyQQSuccess(button);
        }).catch(() => {
            fallbackCopyQQToClipboard(qqNumber, button);
        });
    } else {
        // 降级方案
        fallbackCopyQQToClipboard(qqNumber, button);
    }
}

// 降级复制QQ号方案
function fallbackCopyQQToClipboard(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopyQQSuccess(button);
    } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制QQ号：' + text);
    }
    
    document.body.removeChild(textArea);
}

// 显示QQ号复制成功效果
function showCopyQQSuccess(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="ri-check-line"></i>已复制！';
    button.classList.add('copy-success');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('copy-success');
    }, 2000);
}

// 点击弹窗外部关闭弹窗
document.addEventListener('DOMContentLoaded', function() {
    const emailModal = document.getElementById('emailModal');
    const qqModal = document.getElementById('qqModal');
    
    // 邮箱弹窗事件
    emailModal.addEventListener('click', function(e) {
        if (e.target === emailModal) {
            closeEmailModal();
        }
    });
    
    // QQ弹窗事件
    qqModal.addEventListener('click', function(e) {
        if (e.target === qqModal) {
            closeQQModal();
        }
    });
    
    // ESC键关闭弹窗
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (emailModal.classList.contains('show')) {
                closeEmailModal();
            }
            if (qqModal.classList.contains('show')) {
                closeQQModal();
            }
        }
    });
});

// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化背景图片
    initRandomBackground();
    
    // 初始化导航菜单
    initNavigation();
    
    // 初始化滚动动画
    initScrollAnimations();
    
    // 初始化AI聊天
    initAIChat();
    
    // 初始化返回顶部按钮
    initBackToTop();
    
    // 初始化联系表单
    initContactForm();
});

// 随机背景图片功能
function initRandomBackground() {
    console.log('开始初始化随机背景...');
    const bgContainer = document.querySelector('.bg-container');
    if (!bgContainer) {
        console.error('未找到 .bg-container 元素');
        return;
    }
    console.log('找到背景容器元素');
    
    // 背景图片数组 - 使用PNG格式的图片
    const backgroundImages = [
        'images/bg1.png',
        'images/bg2.png',
        'images/bg3.png',
        'images/bg4.png',
        'images/bg5.png',
      
    ];
    
    // 随机选择一张图片
    const randomIndex = Math.floor(Math.random() * backgroundImages.length);
    const selectedImage = backgroundImages[randomIndex];
    console.log('随机选择的背景图片:', selectedImage, '索引:', randomIndex);
    
    // 创建图片元素
    const imgElement = document.createElement('img');
    imgElement.src = selectedImage;
    imgElement.alt = '背景图片';
    imgElement.classList.add('bg-image');
    
    // 添加到容器
    bgContainer.appendChild(imgElement);
    console.log('图片元素已添加到容器');
    
    // 立即显示图片（不等待加载完成）
    setTimeout(() => {
        imgElement.classList.add('active');
        console.log('已添加active类，图片应该显示');
    }, 100);
    
    // 图片加载完成后的确认
    imgElement.onload = function() {
        console.log('背景图片加载完成:', selectedImage);
    };
    
    // 添加错误处理
    imgElement.onerror = function() {
        console.error('背景图片加载失败:', selectedImage);
        // 如果图片加载失败，尝试使用备用方案
        imgElement.style.backgroundColor = '#6a5acd';
        imgElement.classList.add('active');
    };
    
    // 预加载其他图片，以便下次访问时可以快速切换
    backgroundImages.forEach(imgSrc => {
        if (imgSrc !== selectedImage) {
            const preloadImg = new Image();
            preloadImg.src = imgSrc;
        }
    });
}

// 导航菜单功能
function initNavigation() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // 汉堡菜单动画
            const spans = menuToggle.querySelectorAll('span');
            spans.forEach(span => span.classList.toggle('active'));
        });
        
        // 点击导航链接后关闭菜单
        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    navLinks.classList.remove('active');
                    const spans = menuToggle.querySelectorAll('span');
                    spans.forEach(span => span.classList.remove('active'));
                }
            });
        });
    }
    
    // 平滑滚动到锚点
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // 使用非线性动画滚动
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 滚动时改变导航栏样式
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    });
}

// 滚动动画
function initScrollAnimations() {
    // 检测元素是否在视口中
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
            rect.bottom >= 0
        );
    }
    
    // 需要动画的元素
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    // 初始检查
    animatedElements.forEach(element => {
        if (isInViewport(element)) {
            element.classList.add('animated');
        }
    });
    
    // 滚动时检查
    window.addEventListener('scroll', function() {
        animatedElements.forEach(element => {
            if (isInViewport(element) && !element.classList.contains('animated')) {
                element.classList.add('animated');
            }
        });
    });
    
    // 兴趣标签动画
    const interestItems = document.querySelectorAll('.interest-item');
    interestItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
}

// AI聊天功能
function initAIChat() {
    const chatBox = document.querySelector('.chat-box');
    const chatInput = document.querySelector('.chat-input');
    const sendBtn = document.querySelector('.send-btn');
    
    if (!chatBox || !chatInput || !sendBtn) return;
    
    // 添加消息到聊天框
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
        messageDiv.textContent = content;
        chatBox.appendChild(messageDiv);
        
        // 滚动到底部
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // 发送消息到AI
    async function sendToAI(message) {
        try {
            // 使用本地后端API
            const response = await fetch('http://localhost:3000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || '聊天请求失败');
            }
            
            const aiResponse = data.response;
            addMessage(aiResponse, false);
            
        } catch (error) {
            console.error('AI API错误:', error);
            addMessage(`发生错误: ${error.message}`, false);
        }
    }
    
    // 发送消息
    function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // 添加用户消息
        addMessage(message, true);
        
        // 清空输入框
        chatInput.value = '';
        
        // 显示AI正在输入
        addMessage('正在思考...', false);
        
        // 发送到AI
        sendToAI(message).then(() => {
            // 移除"正在思考"消息
            chatBox.removeChild(chatBox.lastChild);
        });
    }
    
    // 发送按钮点击事件
    sendBtn.addEventListener('click', sendMessage);
    
    // 输入框回车事件
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // 初始欢迎消息
    addMessage('你好！我是AI助手，有什么可以帮助你的吗？', false);
}

// 联系表单功能
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // 显示提交中状态
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.textContent;
        submitBtn.textContent = '提交中...';
        submitBtn.disabled = true;
        
        try {
            // 发送数据到后端API
            const response = await fetch('http://localhost:3000/api/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, message })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || '提交失败');
            }
            
            // 显示成功消息
            alert('留言提交成功！我们会尽快回复您。');
            
            // 清空表单
            contactForm.reset();
        } catch (error) {
            console.error('提交表单错误:', error);
            alert(`提交失败: ${error.message}`);
        } finally {
            // 恢复按钮状态
            submitBtn.textContent = originalBtnText;
            submitBtn.disabled = false;
        }
    });
}

// 返回顶部按钮
function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;
    
    // 滚动显示/隐藏按钮
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    // 点击返回顶部
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // 使用非线性动画滚动到顶部
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 添加CSS动画类
document.head.insertAdjacentHTML('beforeend', `
<style>
/* 汉堡菜单动画 */
.menu-toggle span.active:nth-child(1) {
    transform: translateY(9px) rotate(45deg);
}

.menu-toggle span.active:nth-child(2) {
    opacity: 0;
}

.menu-toggle span.active:nth-child(3) {
    transform: translateY(-9px) rotate(-45deg);
}

/* 导航栏滚动样式 */
.navbar.scrolled {
    background: var(--dark-bg);
    padding: 10px 0;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

/* 滚动动画 */
.animate-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.animate-on-scroll.animated {
    opacity: 1;
    transform: translateY(0);
}
</style>
`);