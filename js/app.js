// 计数器功能
let count = 0;

// 获取 DOM 元素
const countDisplay = document.getElementById('count');
const increaseBtn = document.getElementById('increaseBtn');
const decreaseBtn = document.getElementById('decreaseBtn');
const resetBtn = document.getElementById('resetBtn');

// 更新计数显示
function updateCount() {
    countDisplay.textContent = count;
}

// 增加计数
increaseBtn.addEventListener('click', function() {
    count++;
    updateCount();
});

// 减少计数
decreaseBtn.addEventListener('click', function() {
    count--;
    updateCount();
});

// 重置计数
resetBtn.addEventListener('click', function() {
    count = 0;
    updateCount();
});

// 打招呼功能
const nameInput = document.getElementById('nameInput');
const greetBtn = document.getElementById('greetBtn');
const greeting = document.getElementById('greeting');

greetBtn.addEventListener('click', function() {
    const name = nameInput.value.trim();
    
    if (name === '') {
        greeting.textContent = '请输入你的名字！';
    } else {
        greeting.textContent = `你好，${name}！欢迎学习 JavaScript！`;
    }
});

// 按 Enter 键也可以触发打招呼
nameInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        greetBtn.click();
    }
});

// 页面加载完成后的提示
console.log('JavaScript 已加载成功！');
console.log('打开浏览器的开发者工具（F12）可以看到这条消息。');
