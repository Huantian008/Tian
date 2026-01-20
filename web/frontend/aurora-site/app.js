const root = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('.theme-icon');
const contactForm = document.getElementById('contactForm');
const formStatus = document.getElementById('formStatus');
const navLinks = document.querySelectorAll('.site-nav a');
const sections = [...document.querySelectorAll('section')];
const yearSpan = document.getElementById('year');

function setTheme(mode) {
    if (mode === 'light') {
        root.classList.add('light');
        themeIcon.textContent = '🌙';
    } else {
        root.classList.remove('light');
        themeIcon.textContent = '☀️';
    }
    localStorage.setItem('theme', mode);
}

const storedTheme = localStorage.getItem('theme');
setTheme(storedTheme || 'dark');

themeToggle.addEventListener('click', () => {
    const isLight = root.classList.contains('light');
    setTheme(isLight ? 'dark' : 'light');
});

function handleScrollSpy() {
    const scrollPos = window.scrollY + 120;
    sections.forEach(section => {
        if (section.offsetTop <= scrollPos && section.offsetTop + section.offsetHeight > scrollPos) {
            navLinks.forEach(link => link.classList.remove('active'));
            const active = document.querySelector(`.site-nav a[href="#${section.id}"]`);
            if (active) active.classList.add('active');
        }
    });
}

window.addEventListener('scroll', handleScrollSpy);
handleScrollSpy();

yearSpan.textContent = new Date().getFullYear();

async function sendMessage(payload) {
    try {
        const res = await fetch('http://localhost:3000/api/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            throw new Error(`API 返回状态 ${res.status}`);
        }
        return await res.json();
    } catch (error) {
        console.warn('无法连接到本地 API，改用本地存储。', error);

        const cached = JSON.parse(localStorage.getItem('offlineMessages') || '[]');
        cached.push({ ...payload, id: Date.now(), offline: true });
        localStorage.setItem('offlineMessages', JSON.stringify(cached));

        return { message: '已保存到浏览器，稍后将自动同步。' };
    }
}

if (contactForm) {
    contactForm.addEventListener('submit', async event => {
        event.preventDefault();
        formStatus.textContent = '发送中...';

        const formData = new FormData(contactForm);
        const payload = {
            name: formData.get('name'),
            email: formData.get('email'),
            message: formData.get('message'),
        };

        try {
            await sendMessage(payload);
            formStatus.textContent = '✅ 已收到你的消息！';
            contactForm.reset();
        } catch (error) {
            console.error(error);
            formStatus.textContent = '❌ 发送失败，请稍后再试。';
        }
    });
}
