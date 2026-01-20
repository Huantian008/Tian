# 懂球帝静态站点说明

本项目为 5 个页面的静态网站作业，使用原生 HTML + CSS + JavaScript 实现，布局与交互参考用户提供的截图。

## 目录结构
- `index.html`：主页
- `match.html`：专家预测 / 赛程直播
- `news.html`：动态
- `video.html`：视频
- `about.html`：数据中心
- `css/style.css`：统一样式文件
- `js/`：交互脚本
  - `navbar.js`：滚动高亮导航 + 返回顶部
  - `dropdown.js`：移动端折叠菜单 + 简单筛选
  - `carousel.js`：轮播图
  - `newsFade.js`：进入视口渐显
  - `videoPopup.js`：视频弹窗
- `images/`：页面图片素材

## 页面说明
- 主页（`index.html`）：顶部赛程条、左图右列表的资讯区、热门视频区、数据区块。
- 动态（`news.html`）：大图轮播 + 右侧列表；下方“国内动态/闲情”双栏列表。
- 视频（`video.html`）：大图位 + 右侧竖列小图；下方视频网格与热门列表。
- 赛程直播（`match.html`）：左侧赛事分类，右侧当日赛程列表。
- 数据中心（`about.html`）：联赛侧栏 + 积分榜表格。

## 已实现的 5 个特效
1. 轮播图自动切换与箭头切换（`js/carousel.js`）。
2. 滚动时导航吸顶样式 + 返回顶部按钮显示（`js/navbar.js`）。
3. 移动端折叠菜单（`js/dropdown.js`）。
4. 内容进入视口渐显（`js/newsFade.js`）。
5. 视频卡片点击弹窗播放（`js/videoPopup.js`）。

## 图片使用说明
当前页面已按图片内容进行替换，图片均存放在 `images/` 目录中。
如需替换成新的截图或裁切图，保持文件名或改为新的路径并同步更新 HTML 中的 `<img>`。

## 运行方式
直接用浏览器打开 `index.html`，通过导航跳转到其他页面。

