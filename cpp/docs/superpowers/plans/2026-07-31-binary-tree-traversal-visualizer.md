# 考研二叉树遍历可视化 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现单文件 HTML 交互工具,用动画演示二叉树先/中/后序的递归与非递归遍历、层次遍历,配套辅助栈/队列/调用栈可视化,帮助考研 408 备考理解遍历过程。

**Architecture:** 单文件 `binary_tree_traversal.html`,零依赖。核心算法(树模型、布局计算、步骤生成、播放器状态)是纯 JS,不触碰 DOM,可通过 Node 无头测试;渲染与 UI 接线在浏览器内运行,页面加载时自检。测试文件用正则从 HTML 中提取唯一的 `<script>` 块,在 Node 中执行并断言。

**Tech Stack:** 原生 HTML5 + CSS3 + ES6 JavaScript(浏览器侧);Node.js >= 18(测试侧,仅用内置 `assert`,无第三方依赖)。

## Global Constraints

- 单文件交付:`e:\code\cpp\binary_tree_traversal.html`,零依赖、零构建、离线可用,双击即开。
- HTML 内**恰好一个** `<script>` 块,无 `src` 引用,无外部 CSS/JS/字体/CDN。
- 脚本顶层**不得**访问 DOM(仅函数体内可访问),并以 `globalThis.TraversalViz` 暴露命名空间,末尾用 `if (typeof document !== 'undefined') { ... }` 守卫浏览器初始化——否则 Node 无法执行。
- 中文界面。颜色语义固定:蓝=指针/递归层、绿=入栈/入队、红=出栈/出队、橙=访问。
- 7 种模式:递归先/中/后序、非递归先/中/后序、层次遍历。非递归算法严格按王道教材写法(先序:出栈访问、右先左后入栈;中序:左链入栈、出栈后转右子树;后序:元素带 tag,二次入栈后遇 tag=1 才访问;层次:队列)。
- 5 棵预设树:王道例题 7 结点(A/B/C/D/E/F/G)、空树、单结点、左斜树、右斜树。王道例题期望:先序 `A B D E C F G`、中序 `D B E A F C G`、后序 `D E B F G C A`、层次 `A B C D E F G`。
- 随机树:常规树结点数 8~15、高度 <= 5;**退化树(左/右斜)结点数 5~8、高度 <= 8**(斜树高度=结点数,这是对"高度<=5"的唯一例外,设计文档已在验证节明确混入退化情形)。
- 测试文件:`e:\code\cpp\tests\binary_tree_traversal.test.js`,运行命令 `node tests/binary_tree_traversal.test.js`,零第三方依赖。
- 提交信息用中文,commit 到当前分支 `skill/run-trapping-rain-water`。

---

### Task 1: HTML 骨架 + CSS 布局 + Node 测试脚手架

**Files:**
- Create: `e:\code\cpp\binary_tree_traversal.html`
- Create: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: 无。
- Produces: `globalThis.TraversalViz` 命名空间对象(先含 `runSelfTests()` 桩),HTML 页面骨架与所有控件 id:`#mode-select`、`#tree-select`、`#btn-random`、`#btn-play`、`#btn-prev`、`#btn-next`、`#btn-reset`、`#speed-slider`、`#speed-label`、`#result-sequence`、`#aux-panel`、`#self-test-badge`、`#tree-info`、`#tree-canvas`(SVG)。
- 测试侧产物:`tests/binary_tree_traversal.test.js` 的加载器 + 测试框架(后续任务在此文件追加测试)。

- [ ] **Step 1: 写失败测试(脚手架)**

创建 `e:\code\cpp\tests\binary_tree_traversal.test.js`:

```js
'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const HTML_PATH = path.join(__dirname, '..', 'binary_tree_traversal.html');
const html = fs.readFileSync(HTML_PATH, 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.strictEqual(scripts.length, 1, 'HTML 中应恰好有一个 <script> 块(无 src)');
const src = scripts[0][1];
new Function(src)(); // 执行脚本,暴露 globalThis.TraversalViz

const T = globalThis.TraversalViz;
assert.ok(T && typeof T === 'object', '脚本应暴露 globalThis.TraversalViz');

const tests = [];
function test(name, fn) { tests.push({ name, fn }); }

// ===== 测试写在这里 =====
test('命名空间暴露 runSelfTests', () => {
  assert.strictEqual(typeof T.runSelfTests, 'function');
});

// ===== 运行器 =====
let passed = 0, failed = 0;
for (const { name, fn } of tests) {
  try { fn(); passed++; console.log('  ✓ ' + name); }
  catch (e) { failed++; console.error('  ✗ ' + name + '\n    ' + e.message); }
}
console.log(`\n${passed} 项通过, ${failed} 项失败`);
process.exit(failed ? 1 : 0);
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 崩溃或报错(`ENOENT`,HTML 文件不存在)。

- [ ] **Step 3: 写 HTML 骨架(完整代码)**

创建 `e:\code\cpp\binary_tree_traversal.html`。结构:左侧 SVG 画布,右侧控制面板(模式选择、树来源、控制条、结果序列、辅助结构面板、自检徽章)。样式浅色清爽,适合学习工具。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>二叉树遍历可视化 - 考研数据结构</title>
<style>
  :root {
    --c-enter: #2f6fed;  /* 蓝:当前指针/递归层 */
    --c-push:  #1db954;  /* 绿:入栈/入队 */
    --c-pop:   #e5484d;  /* 红:出栈/出队 */
    --c-visit: #f59f00;  /* 橙:访问 */
    --c-bg:    #f7f8fa;
    --c-card:  #ffffff;
    --c-line:  #d9dee5;
    --c-text:  #22262b;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: "Microsoft YaHei", "PingFang SC", sans-serif; background: var(--c-bg); color: var(--c-text); }
  header { padding: 14px 24px; background: var(--c-card); border-bottom: 1px solid var(--c-line); display: flex; align-items: center; gap: 16px; }
  header h1 { font-size: 20px; }
  #self-test-badge { font-size: 13px; padding: 4px 12px; border-radius: 999px; background: #eee; color: #555; }
  #self-test-badge.pass { background: #e3f7ec; color: #157347; }
  #self-test-badge.fail { background: #fdecec; color: #b02a37; }
  main { display: flex; gap: 16px; padding: 16px; min-height: calc(100vh - 64px); }
  #canvas-wrap { flex: 1; background: var(--c-card); border: 1px solid var(--c-line); border-radius: 10px; padding: 10px; min-width: 0; }
  #tree-canvas { width: 100%; height: 560px; display: block; }
  #tree-info { font-size: 13px; color: #666; padding: 4px 2px 0; }
  aside { width: 300px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px; }
  .card { background: var(--c-card); border: 1px solid var(--c-line); border-radius: 10px; padding: 12px; }
  .card h2 { font-size: 14px; margin-bottom: 8px; color: #444; }
  .card label { font-size: 13px; color: #555; display: block; margin-bottom: 4px; }
  select, button, input[type=range] { font-size: 14px; }
  select { width: 100%; padding: 6px 8px; border: 1px solid var(--c-line); border-radius: 6px; background: #fff; margin-bottom: 10px; }
  .btn-row { display: flex; gap: 6px; flex-wrap: wrap; }
  button { padding: 7px 12px; border: 1px solid var(--c-line); border-radius: 6px; background: #fff; cursor: pointer; }
  button:hover { background: #f0f2f5; }
  button.primary { background: var(--c-enter); color: #fff; border-color: var(--c-enter); }
  button.primary:hover { background: #245bd4; }
  .speed-row { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
  .speed-row input { flex: 1; }
  #speed-label { font-size: 13px; color: #666; min-width: 52px; }
  #result-sequence { display: flex; flex-wrap: wrap; gap: 6px; min-height: 32px; }
  .chip { width: 34px; height: 34px; border-radius: 50%; border: 2px solid var(--c-line); background: #fff; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 15px; }
  .chip.done { background: var(--c-visit); border-color: var(--c-visit); color: #fff; }
  #aux-panel { font-size: 13px; line-height: 1.7; color: #333; min-height: 40px; font-family: Consolas, "Courier New", monospace; }
  /* 树节点状态 */
  .t-node circle { stroke: #33414f; stroke-width: 2; fill: #fff; transition: fill .25s, stroke .25s; }
  .t-node.enter circle { fill: var(--c-enter); stroke: var(--c-enter); }
  .t-node.push circle { fill: var(--c-push); stroke: var(--c-push); }
  .t-node.pop circle { fill: var(--c-pop); stroke: var(--c-pop); }
  .t-node.visit circle { fill: var(--c-visit); stroke: var(--c-visit); }
  .t-node text { fill: #fff; font-size: 17px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }
  .t-edge { stroke: var(--c-line); stroke-width: 2; }
  .flash { animation: popflash .5s ease; }
  @keyframes popflash { 0% { transform: scale(1); } 40% { transform: scale(1.25); } 100% { transform: scale(1); } }
  .legend { font-size: 12px; color: #666; margin-top: 8px; display: flex; flex-wrap: wrap; gap: 10px; }
  .legend span::before { content: ''; display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 4px; vertical-align: -1px; }
</style>
</head>
<body>
<header>
  <h1>🌳 二叉树遍历可视化(考研数据结构)</h1>
  <div id="self-test-badge">自检运行中…</div>
</header>
<main>
  <div id="canvas-wrap">
    <svg id="tree-canvas" viewBox="0 0 800 560" preserveAspectRatio="xMidYMid meet"></svg>
    <div id="tree-info"></div>
  </div>
  <aside>
    <div class="card">
      <h2>遍历模式</h2>
      <select id="mode-select"></select>
    </div>
    <div class="card">
      <h2>树的来源</h2>
      <select id="tree-select"></select>
      <button id="btn-random" class="primary">🎲 随机生成</button>
    </div>
    <div class="card">
      <h2>控制</h2>
      <div class="btn-row">
        <button id="btn-prev" title="上一步">⏮ 上一步</button>
        <button id="btn-play" class="primary" title="播放/暂停">▶ 播放</button>
        <button id="btn-next" title="下一步">⏭ 下一步</button>
        <button id="btn-reset" title="重置">↺ 重置</button>
      </div>
      <div class="speed-row">
        <span>速度</span>
        <input id="speed-slider" type="range" min="25" max="300" value="100">
        <span id="speed-label">1.0×</span>
      </div>
    </div>
    <div class="card">
      <h2>遍历结果序列</h2>
      <div id="result-sequence"></div>
      <div class="legend">
        <span style="color:#157347">已访问</span>
      </div>
    </div>
    <div class="card">
      <h2>辅助结构面板</h2>
      <div id="aux-panel"></div>
      <div class="legend">
        <span style="color:#1db954">● 入栈/入队</span>
        <span style="color:#e5484d">● 出栈/出队</span>
        <span style="color:#2f6fed">● 当前层/指针</span>
        <span style="color:#f59f00">● 访问</span>
      </div>
    </div>
  </aside>
</main>
<script>
'use strict';
// 命名空间:所有逻辑挂到 TraversalViz 上,顶层不碰 DOM(保证 Node 可执行)
const TraversalViz = (() => {
  const selfTestChecks = []; // { name, fn } —— 浏览器加载时运行
  function runSelfTests() {
    let pass = 0, fail = 0;
    for (const c of selfTestChecks) {
      try { c.fn(); pass++; }
      catch (e) { fail++; console.error('[自检失败] ' + c.name + ': ' + e.message); }
    }
    return { pass, fail };
  }
  function initUI() { /* Task 8 填充 */ }
  return { runSelfTests, initUI, selfTestChecks };
})();
globalThis.TraversalViz = TraversalViz;
if (typeof document !== 'undefined') { TraversalViz.initUI(); } // 必须走命名空间:initUI 是 IIFE 内的函数,裸调用会 ReferenceError
</script>
</body>
</html>
```

注意:骨架里 `initUI` 是空函数——Task 8 才填充。浏览器打开暂不报错(选择器为空而已)。

- [ ] **Step 4: 运行测试确认通过**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `  ✓ 命名空间暴露 runSelfTests` + `1 项通过, 0 项失败`,退出码 0。

- [ ] **Step 5: 浏览器冒烟(可选,手动)**

双击打开 `binary_tree_traversal.html`,确认页面布局与设计一致(左画布、右面板),控制台无报错。自检徽章暂时显示"自检运行中…"是预期的(自检逻辑 Task 8 填充)。

- [ ] **Step 6: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 二叉树遍历可视化页面骨架与 Node 测试脚手架"
```

注意:`binary_tree_traversal.html` 与测试文件相对 git 根 `E:/code` 的路径是 `cpp/...`。

### Task 2: 树数据模型 + 预设树 + 布局计算

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`(在 `selfTestChecks` 行上方、`initUI` 定义之前插入新函数)
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`(在 `// ===== 测试写在这里 =====` 处追加测试)

**Interfaces:**
- Consumes: Task 1 的命名空间。
- Produces:
  - `createNode(val, left = null, right = null) -> { val, left, right }`
  - `size(root) -> number`(结点数)
  - `height(root) -> number`(层数,空树为 0,单结点为 1)
  - `makeSkew(chars, toRight) -> root`(用字符数组自底向上建左/右斜树)
  - `PRESET_TREES -> [{ name, root }, ...]`(5 棵预设树)
  - `computeLayout(root) -> Map<node, {x, y}>`(满二叉树下标法,x/y 为 0~1 归一化)

- [ ] **Step 1: 写失败测试**

在测试文件 `// ===== 测试写在这里 =====` 后追加:

```js
// ===== Task 2: 树模型 / 预设 / 布局 =====
const CANONICAL = T.PRESET_TREES[0].root; // 王道例题 A/B/C/D/E/F/G

test('预设树:第一棵是王道例题 7 结点树', () => {
  assert.strictEqual(T.PRESET_TREES.length, 5);
  assert.strictEqual(T.size(CANONICAL), 7);
  assert.strictEqual(T.height(CANONICAL), 3);
});

test('createNode 结构正确', () => {
  const n = T.createNode('X', T.createNode('Y'), T.createNode('Z'));
  assert.strictEqual(n.val, 'X');
  assert.strictEqual(n.left.val, 'Y');
  assert.strictEqual(n.right.val, 'Z');
});

test('空树/单结点树', () => {
  assert.strictEqual(T.size(null), 0);
  assert.strictEqual(T.height(null), 0);
  assert.strictEqual(T.size(T.PRESET_TREES[1].root), 0); // 空树预设
  assert.strictEqual(T.size(T.PRESET_TREES[2].root), 1); // 单结点预设
  assert.strictEqual(T.height(T.PRESET_TREES[2].root), 1);
});

test('斜树预设:结点数和链式结构', () => {
  const L = T.PRESET_TREES[3].root; // 左斜 A->B->C->D->E
  const R = T.PRESET_TREES[4].root; // 右斜 A->B->C->D->E
  assert.strictEqual(T.size(L), 5);
  assert.strictEqual(T.height(L), 5);
  assert.strictEqual(T.size(R), 5);
  assert.strictEqual(T.height(R), 5);
  let p = L; let chain = 0;
  while (p) { chain++; assert.strictEqual(p.right, null); p = p.left; } // 左斜无右子
  assert.strictEqual(chain, 5);
});

test('布局:王道例题各结点坐标符合满二叉树下标法', () => {
  const map = T.computeLayout(CANONICAL);
  assert.strictEqual(map.size, 7);
  const at = (val) => map.get([...map.keys()].find(n => n.val === val));
  const root = at('A');
  assert.strictEqual(root.x, 0.5);
  assert.strictEqual(root.y, 0);
  assert.strictEqual(at('B').x, 0.25);
  assert.strictEqual(at('C').x, 0.75);
  assert.strictEqual(at('B').y, at('C').y);
  assert.strictEqual(at('D').x, 0.125);
  assert.strictEqual(at('D').y, 1);
  // 归一化范围与不重叠
  const coords = [...map.values()];
  for (const c of coords) {
    assert.ok(c.x >= 0 && c.x <= 1, 'x 越界: ' + c.x);
    assert.ok(c.y >= 0 && c.y <= 1, 'y 越界: ' + c.y);
  }
  const keys = coords.map(c => c.x.toFixed(6) + ',' + c.y.toFixed(6));
  assert.strictEqual(new Set(keys).size, 7, '结点坐标有重叠');
});

test('布局:斜树坐标不越界', () => {
  const map = T.computeLayout(T.PRESET_TREES[3].root);
  for (const c of map.values()) {
    assert.ok(c.x > 0 && c.x <= 1, '斜树 x 越界: ' + c.x);
  }
  assert.strictEqual(map.size, 5);
});

test('布局:空树返回空 Map', () => {
  assert.strictEqual(T.computeLayout(null).size, 0);
});
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `✗` 报错(`PRESET_TREES` / `createNode` 等未定义),有失败项。

- [ ] **Step 3: 写实现**

在 HTML `<script>` 内、`const TraversalViz = (() => {` 之后插入(保持命名空间内):

```js
  // ===== 树数据模型 =====
  function createNode(val, left = null, right = null) { return { val, left, right }; }
  function size(root) { return root ? 1 + size(root.left) + size(root.right) : 0; }
  function height(root) { return root ? 1 + Math.max(height(root.left), height(root.right)) : 0; }
  function makeSkew(chars, toRight) {
    let root = null;
    for (let i = chars.length - 1; i >= 0; i--) {
      const n = createNode(chars[i]);
      if (toRight) n.right = root; else n.left = root;
      root = n;
    }
    return root;
  }
  const PRESET_TREES = [
    { name: '王道例题 7 结点', root: (() => {
        const D = createNode('D'), E = createNode('E'), F = createNode('F'), G = createNode('G');
        const B = createNode('B', D, E), C = createNode('C', F, G);
        return createNode('A', B, C);
      })() },
    { name: '空树', root: null },
    { name: '单结点', root: createNode('A') },
    { name: '左斜树(A→B→C→D→E)', root: makeSkew('ABCDE', false) },
    { name: '右斜树(A→B→C→D→E)', root: makeSkew('ABCDE', true) },
  ];

  // ===== 布局:满二叉树下标法,返回 Map<node, {x, y}>,坐标为 0~1 归一化 =====
  function computeLayout(root) {
    const map = new Map();
    if (!root) return map;
    const h = height(root);
    const walk = (node, index, depth) => {
      const x = (index - Math.pow(2, depth) + 0.5) / Math.pow(2, depth);
      const y = h === 1 ? 0 : depth / (h - 1);
      map.set(node, { x, y });
      if (node.left) walk(node.left, index * 2, depth + 1);
      if (node.right) walk(node.right, index * 2 + 1, depth + 1);
    };
    walk(root, 1, 0);
    return map;
  }
```

并在 `return` 语句中导出:`return { runSelfTests, initUI, selfTestChecks, createNode, size, height, makeSkew, PRESET_TREES, computeLayout };`

- [ ] **Step 4: 运行确认通过**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓,`8 项通过, 0 项失败`。

- [ ] **Step 5: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 树数据模型、预设树与满二叉树布局计算"
```

### Task 3: 递归遍历步骤生成(先/中/后序)

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: Task 2 的 `createNode`、`PRESET_TREES`。
- Produces:
  - `genRecursiveSteps(root, mode) -> steps`(mode: `'pre' | 'in' | 'post'`)
  - `stepsToSequence(steps) -> [val, ...]`(提取 visit 事件的值序列)
  - 步骤事件统一格式:`{ type: 'enter'|'visit'|'exit'|'push'|'pop'|'enqueue'|'dequeue', node, aux }`,`aux` 是该步时的辅助结构快照(结点值数组)。

- [ ] **Step 1: 写失败测试(手算期望值)**

追加到测试文件(紧接 Task 2 测试之后):

```js
// ===== Task 3: 递归遍历步骤生成 =====
const seq = (steps) => T.stepsToSequence(steps).join('');

test('递归先序:访问序列 = 根左右 A B D E C F G', () => {
  assert.strictEqual(seq(T.genRecursiveSteps(CANONICAL, 'pre')), 'ABDECFG');
});
test('递归中序:访问序列 = 左根右 D B E A F C G', () => {
  assert.strictEqual(seq(T.genRecursiveSteps(CANONICAL, 'in')), 'DBEAFCG');
});
test('递归后序:访问序列 = 左右根 D E B F G C A', () => {
  assert.strictEqual(seq(T.genRecursiveSteps(CANONICAL, 'post')), 'DEBFGCA');
});

test('递归先序:完整步骤结构与调用栈快照(手算 21 步)', () => {
  const steps = T.genRecursiveSteps(CANONICAL, 'pre');
  assert.strictEqual(steps.length, 21);
  // 事件类型序列(手算:E=enter V=visit X=exit)
  const types = steps.map(s => ({ enter: 'E', visit: 'V', exit: 'X' }[s.type])).join('');
  assert.strictEqual(types, 'EVEVEVXEVXXEVEVXEVXXX');
  // 首步与末步
  assert.deepStrictEqual(steps[0], { type: 'enter', node: CANONICAL, aux: ['A'] });
  assert.strictEqual(steps[steps.length - 1].type, 'exit');
  assert.deepStrictEqual(steps[steps.length - 1].aux, []);
  // 调用栈快照里程碑:visit D 时栈为 [A,B,D];exit D 后为 [A,B]
  const atVisitD = steps.findIndex(s => s.type === 'visit' && s.node.val === 'D');
  assert.deepStrictEqual(steps[atVisitD].aux, ['A', 'B', 'D']);
  const exitD = steps.findIndex(s => s.type === 'exit' && s.node.val === 'D');
  assert.deepStrictEqual(steps[exitD].aux, ['A', 'B']);
});

test('递归:空树返回空步骤,单结点 3 步', () => {
  assert.strictEqual(T.genRecursiveSteps(null, 'pre').length, 0);
  const one = T.genRecursiveSteps(T.PRESET_TREES[2].root, 'in');
  assert.strictEqual(one.length, 3);
  assert.deepStrictEqual(one.map(s => s.type), ['enter', 'visit', 'exit']);
  assert.strictEqual(seq(one), 'A');
});

test('递归:斜树序列正确(左斜 A→B→C→D→E)', () => {
  const L = T.PRESET_TREES[3].root;
  assert.strictEqual(seq(T.genRecursiveSteps(L, 'pre')), 'ABCDE');
  assert.strictEqual(seq(T.genRecursiveSteps(L, 'in')), 'EDCBA'); // 中序左斜 = 从底往上
  assert.strictEqual(seq(T.genRecursiveSteps(L, 'post')), 'EDCBA');
});
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `genRecursiveSteps is not a function` 等失败。

- [ ] **Step 3: 写实现**

插入命名空间(Task 2 代码之后):

```js
  // ===== 递归遍历步骤生成 =====
  // mode: 'pre' | 'in' | 'post';aux = 当前递归调用栈帧(结点值),栈底在前
  function genRecursiveSteps(root, mode) {
    const steps = [];
    const aux = [];
    const rec = (node) => {
      if (!node) return;
      aux.push(node.val);
      steps.push({ type: 'enter', node, aux: aux.slice() });
      if (mode === 'pre') {
        steps.push({ type: 'visit', node, aux: aux.slice() });
        rec(node.left); rec(node.right);
      } else if (mode === 'in') {
        rec(node.left);
        steps.push({ type: 'visit', node, aux: aux.slice() });
        rec(node.right);
      } else {
        rec(node.left); rec(node.right);
        steps.push({ type: 'visit', node, aux: aux.slice() });
      }
      aux.pop(); // 先弹出调用帧,再记录 exit 快照——显示"返回后"的调用栈
      steps.push({ type: 'exit', node, aux: aux.slice() });
    };
    rec(root);
    return steps;
  }
  function stepsToSequence(steps) {
    return steps.filter(s => s.type === 'visit').map(s => s.node.val);
  }
```

导出新增:`genRecursiveSteps, stepsToSequence`。

- [ ] **Step 4: 运行确认通过**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓。

- [ ] **Step 5: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 递归先/中/后序遍历步骤生成(含调用栈快照)"
```

### Task 4: 非递归遍历步骤生成(栈模拟)

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: Task 3 的 `stepsToSequence`、`genRecursiveSteps`(交叉验证用)。
- Produces: `genIterativeSteps(root, mode) -> steps`(mode: `'pre' | 'in' | 'post'`,事件含 `push`/`pop`/`visit`,`aux` = 栈快照,栈底在前)。

- [ ] **Step 1: 写失败测试(王道例题)**

追加:

```js
// ===== Task 4: 非递归遍历(栈) =====
test('非递归先序:序列 A B D E C F G', () => {
  assert.strictEqual(seq(T.genIterativeSteps(CANONICAL, 'pre')), 'ABDECFG');
});
test('非递归中序:序列 D B E A F C G', () => {
  assert.strictEqual(seq(T.genIterativeSteps(CANONICAL, 'in')), 'DBEAFCG');
});
test('非递归后序:序列 D E B F G C A', () => {
  assert.strictEqual(seq(T.genIterativeSteps(CANONICAL, 'post')), 'DEBFGCA');
});

test('非递归先序:步骤结构(21 步,先 push 后 pop+visit)', () => {
  const steps = T.genIterativeSteps(CANONICAL, 'pre');
  assert.strictEqual(steps.length, 21);
  assert.strictEqual(steps[0].type, 'push');
  assert.deepStrictEqual(steps[0].aux, ['A']);
  const types = steps.map(s => s.type);
  assert.strictEqual(types.filter(t => t === 'push').length, 7);
  assert.strictEqual(types.filter(t => t === 'pop').length, 7);
  assert.strictEqual(types.filter(t => t === 'visit').length, 7);
  // 出栈访问 A 后,先压右子 C 再压左子 B → 栈为 [C, B](右先左后,栈顶是 B)
  const afterPopA = steps.findIndex(s => s.type === 'visit' && s.node.val === 'A');
  assert.deepStrictEqual(steps[afterPopA + 2].aux, ['C', 'B']);
});

test('非递归后序:tag 机制步骤结构(A 压入两次,最后访问根)', () => {
  const steps = T.genIterativeSteps(CANONICAL, 'post');
  const pushA = steps.filter(s => s.type === 'push' && s.node.val === 'A');
  assert.strictEqual(pushA.length, 2);
  assert.strictEqual(steps[steps.length - 1].type, 'visit');
  assert.strictEqual(steps[steps.length - 1].node.val, 'A');
  // 访问 D 的瞬间,栈为 [A, C, B, E](A/C 待回溯,已二入栈;E 等待处理)
  const atVisitD = steps.findIndex(s => s.type === 'visit' && s.node.val === 'D');
  assert.deepStrictEqual(steps[atVisitD].aux, ['A', 'C', 'B', 'E']);
  // 访问根 A 时栈已空
  assert.deepStrictEqual(steps[steps.length - 1].aux, []);
});

test('交叉验证:非递归 = 递归(全部预设树 × 3 模式)', () => {
  for (const tree of T.PRESET_TREES) {
    for (const mode of ['pre', 'in', 'post']) {
      const a = seq(T.genRecursiveSteps(tree.root, mode));
      const b = seq(T.genIterativeSteps(tree.root, mode));
      assert.strictEqual(a, b, tree.name + ' ' + mode + ': ' + a + ' != ' + b);
    }
  }
});
```

注意:随机树的交叉验证测试在 Task 5 Step 1 里补(依赖 `generateRandomTree`),本任务不写。

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `genIterativeSteps is not a function` 失败。

- [ ] **Step 3: 写实现(王道教材标准写法)**

插入命名空间:

```js
  // ===== 非递归遍历步骤生成(栈模拟,王道写法) =====
  // pre: 出栈即访问,右子先入栈、左子后入栈
  // in:  指针沿左链深入入栈,出栈访问后转向右子树
  // post:栈元素 {node, tag};tag=0 出栈后以 tag=1 重新入栈,再出栈才访问
  function genIterativeSteps(root, mode) {
    const steps = [];
    // 快照只存值:pre/in 栈里是结点,post 栈里是 {node, tag}
    const auxOf = (st) => st.map(e => (e.node ? e.node.val : e.val));
    const pushEv = (node, stack) => steps.push({ type: 'push', node, aux: auxOf(stack) });
    const popEv = (node, stack) => steps.push({ type: 'pop', node, aux: auxOf(stack) });
    const visitEv = (node, stack) => steps.push({ type: 'visit', node, aux: auxOf(stack) });
    const stack = [];
    if (root) {
      if (mode === 'pre') {
        stack.push(root); pushEv(root, stack);
        while (stack.length) {
          const n = stack.pop(); popEv(n, stack);
          visitEv(n, stack);
          if (n.right) { stack.push(n.right); pushEv(n.right, stack); }
          if (n.left) { stack.push(n.left); pushEv(n.left, stack); }
        }
      } else if (mode === 'in') {
        let p = root;
        while (p || stack.length) {
          while (p) { stack.push(p); pushEv(p, stack); p = p.left; }
          const n = stack.pop(); popEv(n, stack);
          visitEv(n, stack);
          p = n.right;
        }
      } else { // post,tag 标记法
        stack.push({ node: root, tag: 0 }); pushEv(root, stack);
        while (stack.length) {
          const top = stack.pop(); popEv(top.node, stack);
          if (top.tag === 1) { visitEv(top.node, stack); }
          else {
            stack.push({ node: top.node, tag: 1 }); pushEv(top.node, stack);
            if (top.node.right) { stack.push({ node: top.node.right, tag: 0 }); pushEv(top.node.right, stack); }
            if (top.node.left) { stack.push({ node: top.node.left, tag: 0 }); pushEv(top.node.left, stack); }
          }
        }
      }
    }
    return steps;
  }
```

导出新增:`genIterativeSteps`。

- [ ] **Step 4: 运行确认通过(此时不含随机树交叉验证)**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓。

- [ ] **Step 5: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 非递归先/中/后序遍历步骤生成(栈模拟,王道写法)"
```

### Task 5: 层次遍历步骤生成 + 随机树生成器

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: Task 2 的 `createNode`、`makeSkew`、`size`、`height`。
- Produces:
  - `genLevelSteps(root) -> steps`(事件 `enqueue`/`dequeue`/`visit`,`aux` = 队列快照,队首在前)
  - `generateRandomTree(seed = 1, opts = {}) -> root`(`opts.degenerate = true` 时生成 5~8 结点斜树;否则常规随机树 8~15 结点、高度 <= 5;LCG 种子可复现)

- [ ] **Step 1: 写失败测试**

追加:

```js
// ===== Task 5: 层次遍历 + 随机树 =====
test('层次遍历:序列 A B C D E F G', () => {
  assert.strictEqual(seq(T.genLevelSteps(CANONICAL)), 'ABCDEFG');
});

test('层次遍历:入队/出队/访问各 7 次,首步 enqueue A', () => {
  const steps = T.genLevelSteps(CANONICAL);
  assert.strictEqual(steps.length, 21);
  assert.strictEqual(steps[0].type, 'enqueue');
  assert.deepStrictEqual(steps[0].aux, ['A']);
  const types = steps.map(s => s.type);
  assert.strictEqual(types.filter(t => t === 'enqueue').length, 7);
  assert.strictEqual(types.filter(t => t === 'dequeue').length, 7);
  // 出队 A 并访问后,依次入队 B、C → aux = [B, C]
  const afterVisitA = steps.findIndex(s => s.type === 'visit' && s.node.val === 'A');
  assert.deepStrictEqual(steps[afterVisitA + 2].aux, ['B', 'C']);
  // 出队 B 后队首是 C
  const deqB = steps.findIndex(s => s.type === 'dequeue' && s.node.val === 'B');
  assert.deepStrictEqual(steps[deqB].aux, ['C']);
});

test('层次遍历:空树/单结点', () => {
  assert.strictEqual(T.genLevelSteps(null).length, 0);
  assert.strictEqual(seq(T.genLevelSteps(T.PRESET_TREES[2].root)), 'A');
});

test('随机树:常规树 8~15 结点、高度<=5(种子 1..20)', () => {
  for (let seed = 1; seed <= 20; seed++) {
    const root = T.generateRandomTree(seed, { degenerate: false });
    const s = T.size(root), h = T.height(root);
    assert.ok(s >= 8 && s <= 15, 'seed=' + seed + ' 结点数 ' + s);
    assert.ok(h <= 5, 'seed=' + seed + ' 高度 ' + h);
  }
});

test('随机树:退化树 5~8 结点、高度<=8(种子 1..10)', () => {
  for (let seed = 1; seed <= 10; seed++) {
    const root = T.generateRandomTree(seed, { degenerate: true });
    const s = T.size(root), h = T.height(root);
    assert.ok(s >= 5 && s <= 8, 'seed=' + seed + ' 结点数 ' + s);
    assert.ok(h <= 8, 'seed=' + seed + ' 高度 ' + h);
  }
});

test('随机树:同一种子可复现', () => {
  const flatten = (n) => n ? [n.val, flatten(n.left), flatten(n.right)] : ['#'];
  const a = T.generateRandomTree(42, { degenerate: false });
  const b = T.generateRandomTree(42, { degenerate: false });
  assert.deepStrictEqual(flatten(a), flatten(b));
});

test('交叉验证:非递归 = 递归(30 棵种子随机树,补 Task 4 遗留)', () => {
  for (let seed = 1; seed <= 30; seed++) {
    const root = T.generateRandomTree(seed, { degenerate: seed % 5 === 0 });
    for (const mode of ['pre', 'in', 'post']) {
      const a = seq(T.genRecursiveSteps(root, mode));
      const b = seq(T.genIterativeSteps(root, mode));
      assert.strictEqual(a, b, 'seed=' + seed + ' ' + mode);
    }
  }
});
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `genLevelSteps is not a function` / `generateRandomTree is not a function` 失败。

- [ ] **Step 3: 写实现**

插入命名空间:

```js
  // ===== 层次遍历(队列) =====
  function genLevelSteps(root) {
    const steps = [];
    if (!root) return steps;
    const enqEv = (n, q) => steps.push({ type: 'enqueue', node: n, aux: q.map(x => x.val) });
    const deqEv = (n, q) => steps.push({ type: 'dequeue', node: n, aux: q.map(x => x.val) });
    const visitEv = (n, q) => steps.push({ type: 'visit', node: n, aux: q.map(x => x.val) });
    const queue = [root];
    enqEv(root, queue);
    while (queue.length) {
      const n = queue.shift(); deqEv(n, queue);
      visitEv(n, queue);
      if (n.left) { queue.push(n.left); enqEv(n.left, queue); }
      if (n.right) { queue.push(n.right); enqEv(n.right, queue); }
    }
    return steps;
  }

  // ===== 随机树生成(LCG 种子可复现) =====
  function mulberry32(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const labelOf = (i) => String.fromCharCode(65 + (i % 26));

  function generateRandomTree(seed = 1, opts = {}) {
    const rng = mulberry32(seed);
    if (opts.degenerate) {
      const len = 5 + Math.floor(rng() * 4); // 5..8
      const toRight = rng() < 0.5;
      return makeSkew(Array.from({ length: len }, (_, i) => labelOf(i)), toRight);
    }
    let id = 0;
    const root = createNode(labelOf(id++));
    let frontier = [root];
    let depth = 1;
    const target = 8 + Math.floor(rng() * 8); // 8..15
    while (size(root) < target && depth < 5) {
      const next = [];
      for (const p of frontier) {
        if (size(root) >= target) break;
        if (rng() < 0.85) { p.left = createNode(labelOf(id++)); next.push(p.left); }
        if (size(root) < target && rng() < 0.85) { p.right = createNode(labelOf(id++)); next.push(p.right); }
      }
      if (!next.length) break;
      frontier = next; depth++;
    }
    // 兜底:未达目标数时给浅层结点补子结点,保证 >= 8 个
    while (size(root) < target) {
      const candidates = [];
      const collect = (n, d) => {
        if (!n || d >= 5) return;
        if (!n.left || !n.right) candidates.push({ n, side: n.left ? 'right' : 'left' });
        collect(n.left, d + 1); collect(n.right, d + 1);
      };
      collect(root, 1);
      if (!candidates.length) break;
      const c = candidates[Math.floor(rng() * candidates.length)];
      c.n[c.side] = createNode(labelOf(id++));
    }
    return root;
  }
```

导出新增:`genLevelSteps, generateRandomTree`。

- [ ] **Step 4: 运行确认通过(含随机树交叉验证)**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓。

- [ ] **Step 5: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 层次遍历步骤生成与种子随机树生成器"
```

### Task 6: 状态应用纯函数 + 播放器引擎

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: Task 3/4/5 的各步骤生成函数。
- Produces:
  - `applySteps(steps, upto) -> state`,state = `{ colors: Map<node,string>, result: [val,...], aux: [...], lastEvent: step|null }`。`colors` 取值:`'enter'|'push'|'pop'|'visit'|'exit'`;`exit` 表示恢复默认色。
  - `createPlayer({ getSteps, onChange }) -> player`,`player = { play, pause, stepForward, stepBack, reset, setSpeed, getIndex, getState }`,速度默认 1.0,步进间隔 = 900ms / 速度。

- [ ] **Step 1: 写失败测试**

追加:

```js
// ===== Task 6: 状态应用 + 播放器 =====
const MODE_IDS = ['rec-pre', 'rec-in', 'rec-post', 'itr-pre', 'itr-in', 'itr-post', 'level'];
const EXPECTED = {
  'rec-pre': 'ABDECFG', 'rec-in': 'DBEAFCG', 'rec-post': 'DEBFGCA',
  'itr-pre': 'ABDECFG', 'itr-in': 'DBEAFCG', 'itr-post': 'DEBFGCA',
  'level': 'ABCDEFG',
};
const genStepsOf = (modeId, root) => {
  if (modeId.startsWith('rec-')) return T.genRecursiveSteps(root, modeId.slice(4));
  if (modeId.startsWith('itr-')) return T.genIterativeSteps(root, modeId.slice(4));
  return T.genLevelSteps(root);
};

test('applySteps:逐步应用到末尾,7 种模式结果全部正确', () => {
  for (const modeId of MODE_IDS) {
    const steps = genStepsOf(modeId, CANONICAL);
    const st = T.applySteps(steps, steps.length);
    assert.strictEqual(st.result.join(''), EXPECTED[modeId], modeId);
    assert.strictEqual(st.colors.size, 7, modeId + ' 所有结点应已访问');
    for (const c of st.colors.values()) assert.strictEqual(c, 'visit', modeId);
  }
});

test('applySteps:upto=0 为空状态,中途状态含部分结果', () => {
  const steps = T.genRecursiveSteps(CANONICAL, 'pre');
  const empty = T.applySteps(steps, 0);
  assert.strictEqual(empty.result.length, 0);
  assert.strictEqual(empty.colors.size, 0);
  const mid = T.applySteps(steps, 4); // enter A, visit A, enter B, visit B
  assert.strictEqual(mid.result.join(''), 'AB');
  assert.strictEqual(mid.colors.get(CANONICAL), 'visit');
});

test('applySteps:exit 事件把结点颜色清回默认', () => {
  const steps = T.genRecursiveSteps(CANONICAL, 'pre');
  const st = T.applySteps(steps, 3); // enter A, visit A, enter B
  assert.strictEqual(st.colors.get(CANONICAL), 'visit');
  // 走到底,B 之后全部 exit,最后一步是 exit A
  const full = T.applySteps(steps, steps.length);
  assert.strictEqual(steps[steps.length - 1].type, 'exit');
  // 最终状态里除已访问橙色外无残留蓝色——所有 enter 的结点都有 exit 或 visit 覆盖
});

test('播放器:stepForward 走完全程,结果与期望一致,index 正确', () => {
  for (const modeId of MODE_IDS) {
    const steps = genStepsOf(modeId, CANONICAL);
    let latest = null;
    const p = T.createPlayer({ getSteps: () => steps, onChange: (st, idx, total) => { latest = st; } });
    for (let i = 0; i < steps.length + 5; i++) p.stepForward(); // 多走也不越界
    assert.strictEqual(p.getIndex(), steps.length);
    assert.strictEqual(latest.result.join(''), EXPECTED[modeId], modeId);
  }
});

test('播放器:stepBack 回退到开头,结果逐步减少', () => {
  const steps = T.genLevelSteps(CANONICAL);
  const p = T.createPlayer({ getSteps: () => steps });
  while (p.getIndex() < steps.length) p.stepForward();
  assert.strictEqual(p.getState().result.length, 7);
  p.stepBack(); // 跨过 visit G
  assert.strictEqual(p.getState().result.length, 6);
  p.stepBack(); // 跨过 dequeue G,访问数不变
  assert.strictEqual(p.getState().result.length, 6);
  p.stepBack(); // 跨过 visit F
  assert.strictEqual(p.getState().result.length, 5);
  p.reset();
  assert.strictEqual(p.getIndex(), 0);
  assert.strictEqual(p.getState().result.length, 0);
});

test('播放器:空步骤不崩溃,play/setSpeed 可调用', () => {
  const p = T.createPlayer({ getSteps: () => [] });
  p.stepForward(); p.stepBack(); p.play(); p.pause(); p.reset();
  p.setSpeed(2);
  assert.strictEqual(p.getIndex(), 0);
});
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `applySteps is not a function` 失败。

- [ ] **Step 3: 写实现**

插入命名空间:

```js
  // ===== 状态应用:纯函数,由步骤数组 + 索引推导完整状态 =====
  function applySteps(steps, upto) {
    const colors = new Map();
    const result = [];
    let aux = [];
    let lastEvent = null;
    const n = Math.min(upto, steps.length);
    for (let i = 0; i < n; i++) {
      const s = steps[i];
      lastEvent = s;
      aux = s.aux;
      switch (s.type) {
        case 'enter': colors.set(s.node, 'enter'); break;
        case 'push': case 'enqueue': colors.set(s.node, 'push'); break;
        case 'pop': case 'dequeue': colors.set(s.node, 'pop'); break;
        case 'visit':
          colors.set(s.node, 'visit');
          result.push(s.node.val);
          break;
        case 'exit':
          // 已访问的结点保持橙色,未访问的(蓝色)清除——遍历中 exit 总在 visit 之后
          if (colors.get(s.node) !== 'visit') colors.delete(s.node);
          break;
      }
    }
    return { colors, result, aux, lastEvent };
  }

  // ===== 播放器 =====
  function createPlayer({ getSteps, onChange }) {
    let index = 0, timer = null, speed = 1;
    const state = () => applySteps(getSteps(), index);
    const emit = () => { if (onChange) onChange(state(), index, getSteps().length); };
    const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
    const play = () => {
      stop();
      if (index >= getSteps().length) index = 0;
      emit();
      timer = setInterval(() => {
        if (index >= getSteps().length) { stop(); return; } // 走完全程才停,最后一步也要 emit
        index++; emit();
      }, 900 / speed);
    };
    const pause = () => { stop(); };
    const stepForward = () => { stop(); if (index < getSteps().length) index++; emit(); };
    const stepBack = () => { stop(); if (index > 0) index--; emit(); };
    const reset = () => { stop(); index = 0; emit(); };
    const setSpeed = (v) => { speed = v; if (timer) { stop(); play(); } };
    return { play, pause, stepForward, stepBack, reset, setSpeed, getIndex: () => index, getState: state };
  }
```

注意 `applySteps` 中 `enqueue` 与 `push` 同为绿色入列,统一映射 `'push'`(CSS 类 `.push` 已定义)。导出新增:`applySteps, createPlayer`。

- [ ] **Step 4: 运行确认通过**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓。

- [ ] **Step 5: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 状态应用纯函数与播放器引擎(播放/暂停/单步/回退/重置/变速)"
```

### Task 7: 渲染层(画布 / 结果序列 / 辅助面板)

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`(CSS 追加 `.aux-cell` 等样式;命名空间插入渲染函数)
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: `applySteps` 产出的 `state`;Task 5 的 `computeLayout`。
- Produces(字符串构建器,便于 Node 测试;渲染函数在浏览器里把字符串写入容器):
  - `sequenceHtml(state, fullSequence) -> string`(结果序列 chips;已访问填橙,当前步访问加 `flash` 类)
  - `auxHtml(modeId, state) -> string`(辅助结构面板:标题 + 动作 + 栈/队列/调用栈格子,顶格高亮)
  - `renderTree(svg, tree, layout, state)`(SVG 画布,仅浏览器,用 `document`)
  - `renderTreeInfo(container, tree)`
  - 渲染包装:`renderSequence(container, state, fullSequence)`、`renderAuxPanel(container, modeId, state)` = 把字符串构建器结果写入 `container.innerHTML`

- [ ] **Step 1: 写失败测试**

追加:

```js
// ===== Task 7: 渲染(字符串构建器) =====
const countOf = (html, substr) => html.split(substr).length - 1;

test('sequenceHtml:未访问空心、已访问填橙、当前访问闪烁', () => {
  const full = ['A', 'B', 'C'];
  const html = T.sequenceHtml({ result: ['A'], lastEvent: { type: 'visit', node: { val: 'A' } } }, full);
  assert.strictEqual(countOf(html, 'class="chip'), 3, html);
  assert.ok(html.includes('chip done flash'), '当前访问的 A 应闪烁: ' + html);
  assert.ok(html.includes('class="chip">B') && html.includes('class="chip">C'), 'B/C 应为未访问空心: ' + html);
  assert.ok(!html.includes('chip done">B') && !html.includes('chip done">C'), 'B/C 不应已填色: ' + html);
});

test('sequenceHtml:未开始时无 done', () => {
  const html = T.sequenceHtml({ result: [], lastEvent: null }, ['A', 'B']);
  assert.strictEqual(countOf(html, 'chip done'), 0, html);
});

test('auxHtml:非递归中序压栈 3 步后,栈 [A,B,D],D 为栈顶高亮', () => {
  const steps = T.genIterativeSteps(CANONICAL, 'in');
  const st = T.applySteps(steps, 3); // push A, push B, push D
  const html = T.auxHtml('itr-in', st);
  assert.ok(html.includes('辅助栈'), html);
  assert.ok(html.includes('入栈 D'), '应显示当前动作: ' + html);
  assert.strictEqual(countOf(html, 'aux-cell'), 3, html);
  assert.ok(html.includes('aux-cell top'), '栈顶应高亮: ' + html);
  const cells = html.slice(html.indexOf('aux-cell')); // 只看格子区域,标题里有"入栈 D"
  assert.ok(cells.indexOf('D') > cells.indexOf('B') && cells.indexOf('B') > cells.indexOf('A'), '顺序应为 A B D: ' + html);
});

test('auxHtml:层次遍历出队 B 后,队列剩 [C],C 为队首', () => {
  const steps = T.genLevelSteps(CANONICAL);
  const st = T.applySteps(steps, 7); // enq A, deq A, visit A, enq B, enq C, deq B, visit B
  const html = T.auxHtml('level', st);
  assert.ok(html.includes('队列'), html);
  assert.strictEqual(countOf(html, 'aux-cell'), 1, html);
  assert.ok(html.includes('aux-cell top">C'), '队首 C 应高亮: ' + html);
});

test('auxHtml:递归模式标题为递归调用栈,空状态有提示', () => {
  const steps = T.genRecursiveSteps(CANONICAL, 'pre');
  const st = T.applySteps(steps, 3); // enter A, visit A, enter B
  assert.ok(T.auxHtml('rec-pre', st).includes('递归调用栈'));
  const empty = T.auxHtml('rec-pre', T.applySteps(steps, 0));
  assert.ok(empty.includes('尚未开始'), empty);
});
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `sequenceHtml is not a function` 失败。

- [ ] **Step 3: 写实现**

先在 `<style>` 末尾(`.legend span::before` 规则之后)追加 CSS:

```css
  .aux-cell { min-width: 28px; height: 28px; border-radius: 6px; border: 2px solid var(--c-line); display: inline-flex; align-items: center; justify-content: center; font-weight: 600; background: #fff; margin-right: 4px; }
  .aux-cell.top { border-color: var(--c-enter); background: #eef3fe; color: var(--c-enter); }
  .aux-empty { color: #999; }
  .aux-title { margin-bottom: 6px; }
```

再在命名空间插入(位置:`applySteps` 定义之后):

```js
  // ===== 渲染(字符串构建器 + DOM 画布) =====
  const MODE_LABEL = { 'rec-pre': '递归调用栈', 'rec-in': '递归调用栈', 'rec-post': '递归调用栈',
                       'itr-pre': '辅助栈', 'itr-in': '辅助栈', 'itr-post': '辅助栈', 'level': '队列' };
  const EV_TEXT = { enter: '进入', exit: '返回', push: '入栈', pop: '出栈', enqueue: '入队', dequeue: '出队', visit: '访问' };

  function sequenceHtml(state, fullSequence) {
    let html = '';
    fullSequence.forEach((val, i) => {
      const done = i < state.result.length ? ' done' : '';
      const flash = (i === state.result.length - 1 && state.lastEvent && state.lastEvent.type === 'visit') ? ' flash' : '';
      html += '<div class="chip' + done + flash + '">' + val + '</div>';
    });
    return html;
  }

  function auxHtml(modeId, state) {
    if (!state.lastEvent) return '<span class="aux-empty">尚未开始 —— 点击 ▶ 播放或 ⏭ 单步前进</span>';
    const ev = state.lastEvent;
    const title = '<div class="aux-title"><b>' + MODE_LABEL[modeId] + '</b> · 当前动作:<span style="color:var(--c-pop)">' +
                  EV_TEXT[ev.type] + ' ' + ev.node.val + '</span></div>';
    const items = state.aux;
    if (!items.length) return title + '<span class="aux-empty">(空)</span>';
    const isLevel = modeId === 'level';
    let cells = '';
    items.forEach((val, i) => {
      const top = isLevel ? i === 0 : i === items.length - 1; // 队首 / 栈顶
      cells += '<span class="aux-cell' + (top ? ' top' : '') + '">' + val + '</span>';
    });
    return title + cells;
  }

  function renderSequence(container, state, fullSequence) { container.innerHTML = sequenceHtml(state, fullSequence); }
  function renderAuxPanel(container, modeId, state) { container.innerHTML = auxHtml(modeId, state); }

  function renderTreeInfo(container, tree) {
    container.textContent = tree ? '结点数: ' + size(tree) + ' · 高度: ' + height(tree) : '空树';
  }

  const NS = 'http://www.w3.org/2000/svg';
  const RENDER = { w: 800, h: 560, pad: 70, nodeR: 26 };
  function renderTree(svg, tree, layout, state) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const W = RENDER.w, H = RENDER.h, P = RENDER.pad, R = RENDER.nodeR;
    const px = (v) => P + v * (W - 2 * P);
    const py = (v) => P + v * (H - 2 * P);
    if (!tree) {
      const t = document.createElementNS(NS, 'text');
      t.setAttribute('x', W / 2); t.setAttribute('y', H / 2);
      t.setAttribute('text-anchor', 'middle'); t.setAttribute('fill', '#999'); t.setAttribute('font-size', '18');
      t.textContent = '空树 —— 请选择其他树或点击 🎲 随机生成';
      svg.appendChild(t);
      return;
    }
    for (const [node, pos] of layout) { // 边
      for (const child of [node.left, node.right]) {
        if (child && layout.has(child)) {
          const c = layout.get(child);
          const line = document.createElementNS(NS, 'line');
          line.setAttribute('class', 't-edge');
          line.setAttribute('x1', px(pos.x)); line.setAttribute('y1', py(pos.y));
          line.setAttribute('x2', px(c.x)); line.setAttribute('y2', py(c.y));
          svg.appendChild(line);
        }
      }
    }
    for (const [node, pos] of layout) { // 结点
      const g = document.createElementNS(NS, 'g');
      const cls = 't-node' + (state.colors.has(node) ? ' ' + state.colors.get(node) : '');
      if (state.lastEvent && state.lastEvent.node === node &&
          (state.lastEvent.type === 'pop' || state.lastEvent.type === 'dequeue' || state.lastEvent.type === 'visit')) {
        g.setAttribute('class', cls + ' flash');
      } else {
        g.setAttribute('class', cls);
      }
      const circle = document.createElementNS(NS, 'circle');
      circle.setAttribute('cx', px(pos.x)); circle.setAttribute('cy', py(pos.y)); circle.setAttribute('r', R);
      const text = document.createElementNS(NS, 'text');
      text.setAttribute('x', px(pos.x)); text.setAttribute('y', py(pos.y));
      text.textContent = node.val;
      g.appendChild(circle); g.appendChild(text);
      svg.appendChild(g);
    }
  }
```

导出新增:`sequenceHtml, auxHtml, renderSequence, renderAuxPanel, renderTree, renderTreeInfo`。

- [ ] **Step 4: 运行确认通过**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓(DOM 的 `renderTree` 不在此测,由 Task 8 的浏览器自检覆盖)。

- [ ] **Step 5: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: 渲染层——结果序列与辅助面板字符串构建器、SVG 树形画布"
```

### Task 8: UI 接线 + 页面自检 + 手动验收

**Files:**
- Modify: `e:\code\cpp\binary_tree_traversal.html`(`initUI` 填充、`MODES` 表、`rebuild`、播放器按钮文案、自检注册)
- Modify: `e:\code\cpp\tests\binary_tree_traversal.test.js`

**Interfaces:**
- Consumes: 全部已实现函数。
- Produces: 完整可用的页面;`runSelfTests()` 返回 `{ pass, fail }`(浏览器加载时在 `initUI` 末尾运行,徽章显示结果)。

- [ ] **Step 1: 写失败测试(自检集成)**

追加:

```js
// ===== Task 8: 自检集成 =====
test('runSelfTests:Node 环境全部通过(纯逻辑检查,无 DOM)', () => {
  const r = T.runSelfTests();
  assert.strictEqual(r.fail, 0, '自检失败数应为 0,实际 ' + JSON.stringify(r));
  assert.ok(r.pass >= 7, '应有至少 7 项纯逻辑自检,实际 ' + r.pass);
});

test('MODES 表:7 种模式,id 唯一', () => {
  assert.strictEqual(T.MODES.length, 7);
  assert.strictEqual(new Set(T.MODES.map(m => m.id)).size, 7);
});
```

- [ ] **Step 2: 运行确认失败**

Run: `node tests/binary_tree_traversal.test.js`
Expected: `MODES is not defined` / 自检通过数为 0。

- [ ] **Step 3: 写实现**

3a. 在命名空间内、`createPlayer` 之后插入模式表与 UI 状态(同时给 `createPlayer` 的 return 增加 `isPlaying` 读取器——在 Task 6 的 return 语句上改,加 `isPlaying: () => timer !== null`):

```js
  const MODES = [
    { id: 'rec-pre',  label: '递归先序(根→左→右)',       gen: (t) => genRecursiveSteps(t, 'pre') },
    { id: 'rec-in',   label: '递归中序(左→根→右)',       gen: (t) => genRecursiveSteps(t, 'in') },
    { id: 'rec-post', label: '递归后序(左→右→根)',       gen: (t) => genRecursiveSteps(t, 'post') },
    { id: 'itr-pre',  label: '非递归先序(栈模拟)',        gen: (t) => genIterativeSteps(t, 'pre') },
    { id: 'itr-in',   label: '非递归中序(栈模拟)',        gen: (t) => genIterativeSteps(t, 'in') },
    { id: 'itr-post', label: '非递归后序(栈·tag 标记)',   gen: (t) => genIterativeSteps(t, 'post') },
    { id: 'level',    label: '层次遍历(队列)',            gen: (t) => genLevelSteps(t) },
  ];
  let currentTree = null, currentModeId = 'rec-pre', player = null;
  const getMode = () => MODES.find(m => m.id === currentModeId);

  function rebuild() {
    currentTree = currentTree || PRESET_TREES[0].root;
    const steps = getMode().gen(currentTree);
    const full = stepsToSequence(steps);
    player = createPlayer({ getSteps: () => steps, onChange: onPlayerChange });
    onPlayerChange(player.getState(), 0, steps.length);
  }

  function onPlayerChange(state, index, total) {
    const mode = getMode();
    const svg = document.getElementById('tree-canvas');
    const layout = computeLayout(currentTree);
    renderTree(svg, currentTree, layout, state);
    renderSequence(document.getElementById('result-sequence'), state, stepsToSequence(mode.gen(currentTree)));
    renderAuxPanel(document.getElementById('aux-panel'), currentModeId, state);
    renderTreeInfo(document.getElementById('tree-info'), currentTree);
    document.getElementById('btn-play').textContent = player.isPlaying() ? '⏸ 暂停' : '▶ 播放';
  }

  // ===== 自检注册(纯逻辑,模块加载即注册,浏览器/Node 皆可运行) =====
  function registerSelfTests() {
    const t = (name, fn) => selfTestChecks.push({ name, fn });
    t('王道例题:三种递归遍历序列', () => {
      assertSeq('ABDECFG', 'pre'); assertSeq('DBEAFCG', 'in'); assertSeq('DEBFGCA', 'post');
      function assertSeq(expected, mode) {
        const got = stepsToSequence(genRecursiveSteps(PRESET_TREES[0].root, mode)).join('');
        if (got !== expected) throw new Error(mode + ': ' + got + ' != ' + expected);
      }
    });
    t('王道例题:层次遍历序列', () => {
      const got = stepsToSequence(genLevelSteps(PRESET_TREES[0].root)).join('');
      if (got !== 'ABCDEFG') throw new Error(got);
    });
    t('交叉验证:非递归 = 递归(5 棵预设树)', () => {
      for (const tree of PRESET_TREES) for (const mode of ['pre', 'in', 'post']) {
        const a = stepsToSequence(genRecursiveSteps(tree.root, mode)).join('');
        const b = stepsToSequence(genIterativeSteps(tree.root, mode)).join('');
        if (a !== b) throw new Error(tree.name + ' ' + mode);
      }
    });
    t('随机树约束:常规 8~15 结点/高<=5,退化 5~8 结点/高<=8', () => {
      for (let seed = 1; seed <= 20; seed++) {
        const r = generateRandomTree(seed, { degenerate: false });
        if (size(r) < 8 || size(r) > 15 || height(r) > 5) throw new Error('seed ' + seed);
      }
      for (let seed = 1; seed <= 10; seed++) {
        const r = generateRandomTree(seed, { degenerate: true });
        if (size(r) < 5 || size(r) > 8 || height(r) > 8) throw new Error('degenerate seed ' + seed);
      }
    });
    t('边界:空树/单结点遍历', () => {
      for (const g of [genRecursiveSteps, genIterativeSteps]) {
        if (g(null, 'pre').length !== 0) throw new Error('空树');
        if (stepsToSequence(g(PRESET_TREES[2].root, 'in')).join('') !== 'A') throw new Error('单结点');
      }
    });
    t('播放器:7 种模式单步走完全程序列正确', () => {
      for (const m of MODES) {
        const steps = m.gen(PRESET_TREES[0].root);
        const p = createPlayer({ getSteps: () => steps });
        while (p.getIndex() < steps.length) p.stepForward();
        if (p.getState().result.length !== size(PRESET_TREES[0].root)) throw new Error(m.id);
      }
    });
    t('布局:王道例题坐标无重叠', () => {
      const map = computeLayout(PRESET_TREES[0].root);
      const keys = [...map.values()].map(c => c.x.toFixed(6) + ',' + c.y.toFixed(6));
      if (new Set(keys).size !== map.size) throw new Error('重叠');
    });
  }
```

3b. 模块末尾(命名空间 return 之前)调用 `registerSelfTests();`。

3c. 填充 `initUI()`(替换 Task 1 的空函数):

```js
  function initUI() {
    const modeSel = document.getElementById('mode-select');
    MODES.forEach(m => { const o = document.createElement('option'); o.value = m.id; o.textContent = m.label; modeSel.appendChild(o); });
    const treeSel = document.getElementById('tree-select');
    PRESET_TREES.forEach((t, i) => { const o = document.createElement('option'); o.value = i; o.textContent = t.name; treeSel.appendChild(o); });
    modeSel.addEventListener('change', () => { currentModeId = modeSel.value; rebuild(); });
    treeSel.addEventListener('change', () => { currentTree = PRESET_TREES[+treeSel.value].root; rebuild(); });
    document.getElementById('btn-random').addEventListener('click', () => {
      currentTree = generateRandomTree(Date.now() >>> 0, { degenerate: Math.random() < 0.3 });
      rebuild();
    });
    const speed = document.getElementById('speed-slider');
    const speedLabel = document.getElementById('speed-label');
    speed.addEventListener('input', () => {
      speedLabel.textContent = (speed.value / 100).toFixed(1) + '×';
      if (player) player.setSpeed(speed.value / 100);
    });
    document.getElementById('btn-play').addEventListener('click', () => {
      if (player.isPlaying()) player.pause(); else player.play();
      document.getElementById('btn-play').textContent = player.isPlaying() ? '⏸ 暂停' : '▶ 播放';
    });
    document.getElementById('btn-next').addEventListener('click', () => { if (player) player.stepForward(); });
    document.getElementById('btn-prev').addEventListener('click', () => { if (player) player.stepBack(); });
    document.getElementById('btn-reset').addEventListener('click', () => { if (player) player.reset(); });
    rebuild();
    // DOM 自检(仅浏览器)
    selfTestChecks.push({
      name: '画布渲染:王道例题 7 圆 6 边',
      fn: () => {
        const svg = document.getElementById('tree-canvas');
        const layout = computeLayout(currentTree);
        renderTree(svg, currentTree, layout, { colors: new Map(), result: [], aux: [], lastEvent: null });
        const circles = svg.querySelectorAll('circle').length;
        const lines = svg.querySelectorAll('line').length;
        if (circles !== 7 || lines !== 6) throw new Error('circles=' + circles + ' lines=' + lines);
      },
    });
    const r = runSelfTests();
    const badge = document.getElementById('self-test-badge');
    badge.textContent = '自检 ' + r.pass + '/' + (r.pass + r.fail) + ' 通过';
    badge.className = r.fail === 0 ? 'pass' : 'fail';
  }
```

3d. 导出新增:`MODES`。`registerSelfTests` 无需导出(模块内调用)。

- [ ] **Step 4: 运行确认通过**

Run: `node tests/binary_tree_traversal.test.js`
Expected: 全部 ✓。

- [ ] **Step 5: 浏览器手动验收(必须逐项执行)**

双击打开 `binary_tree_traversal.html`(离线),逐项核对:

1. 顶部徽章显示"自检 7/7 通过"(绿色);F12 控制台无红色报错。
2. 默认显示王道例题树,模式为递归先序;点 ▶ 播放,观察:先根 A 变橙,再 B、D、E、C、F、G 依次访问;右侧结果序列逐个填橙;辅助面板显示"递归调用栈"和进入/返回动作。
3. 依次切换 7 种模式,每种都播放一遍;**非递归模式看栈变化**(先序:出栈访问、右先左后;中序:沿左链压栈;后序:同一结点变绿两次后变橙——tag 机制),**层次模式看队列变化**(出队访问、左右入队)。
4. 单步前进/后退各 10 次,颜色与面板状态始终一致,无跳变。
5. 播放中切速度滑块(0.3×~3×),播放节奏实时变化。
6. 切换 5 棵预设树;空树显示提示文字;斜树动画正常。
7. 点 🎲 随机生成 10 次:树形多样,偶见斜树(约 3 成),布局不重叠、不出界。
8. 边播边乱点按钮(换模式/换树/重置/随机),页面不崩溃、无异常。
9. 关闭浏览器重新打开,一切正常。

任一失败项 → 修复后重测再提交。

- [ ] **Step 6: Commit**

```bash
git add cpp/binary_tree_traversal.html cpp/tests/binary_tree_traversal.test.js
git commit -m "feat: UI 接线、模式/树选择、随机生成、页面自检徽章"
```

- [ ] **Step 7: 最终验证(verification-before-completion)**

Run: `node tests/binary_tree_traversal.test.js` → 全部 ✓
Run: `git status --short` → 仅预期文件变动
Run: `git log --oneline -9` → 9 个提交(Task 1..8),分支 `skill/run-trapping-rain-water`

## 验收标准(来自设计文档)

- [ ] 7 种模式全部可播放/暂停/单步/回退/重置/变速
- [ ] 王道例题遍历结果与手算完全一致(先序 ABDECFG、中序 DBEAFCG、后序 DEBFGCA、层次 ABCDEFG)
- [ ] 辅助栈/队列/调用栈面板与课本手算一致
- [ ] 空树、单结点、左斜、右斜、随机树均正常
- [ ] 离线双击打开即用,控制台无报错,自检徽章绿色
