// DOM元素加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const changeTextBtn = document.getElementById('changeTextBtn');
    const myparagraph = document.getElementById('myparagraph');
    const submitBtn = document.getElementById('submitBtn');
    const messageForm = document.getElementById('messageForm');
    const backToTopBtn = document.getElementById('backToTopBtn');
    
    // 改变文本按钮点击事件
    if (changeTextBtn) {
        changeTextBtn.addEventListener('click', changeText);
    }
    
    // 提交表单事件
    if (messageForm) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitMessage();
        });
    }
    
    // 返回顶部按钮点击事件
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function(event) {
            event.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // 添加滚动事件，控制返回顶部按钮的显示
    window.addEventListener('scroll', toggleBackToTopButton);
    
    // 初始化页面时检查按钮状态
    toggleBackToTopButton();
    
    // 为兴趣列表项添加动画效果
    const interestItems = document.querySelectorAll('.interests-list li');
    if (interestItems.length > 0) {
        interestItems.forEach(function(item, index) {
            item.style.animationDelay = (index * 0.2) + 's';
            item.classList.add('fade-in');
        });
    }
});

// 改变文本函数
function changeText() {
    const paragraph = document.getElementById("myparagraph");
    if (paragraph.textContent === "欢迎来到我的个人网站") {
        paragraph.textContent = "Hello World!";
    } else {
        paragraph.textContent = "欢迎来到我的个人网站";
    }
    
    // 添加动画效果
    paragraph.classList.add('text-animation');
    setTimeout(function() {
        paragraph.classList.remove('text-animation');
    }, 1000);
}

// 提交留言函数
function submitMessage() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // 在实际应用中，这里应该发送数据到服务器
    // 这里仅做演示，显示一个提交成功的消息
    alert(`留言提交成功！\n姓名: ${name}\n邮箱: ${email}\n留言: ${message}`);
    
    // 清空表单
    document.getElementById('messageForm').reset();
}

// 控制返回顶部按钮的显示
function toggleBackToTopButton() {
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (!backToTopBtn) return;
    
    if (window.scrollY > 300) {
        backToTopBtn.parentElement.classList.add('visible');
    } else {
        backToTopBtn.parentElement.classList.remove('visible');
    }
}

// 添加CSS动画类
document.head.insertAdjacentHTML('beforeend', `
<style>
.text-animation {
    animation: pulse 1s ease;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.fade-in {
    opacity: 0;
    animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.back-to-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s, visibility 0.3s;
}

.back-to-top.visible {
    opacity: 1;
    visibility: visible;
}

.back-to-top a {
    display: block;
    background-color: #ff5a6a;
    color: white;
    padding: 10px 15px;
    border-radius: 5px;
    text-decoration: none;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}



.project-item {
    padding: 10px;
    border-left: 3px solid #7decea88;
    margin-bottom: 10px;
}

.highlight {
    color: #ff5a6a;
    font-weight: bold;
}
</style>
`);