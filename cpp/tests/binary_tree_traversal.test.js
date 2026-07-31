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

// ===== 运行器 =====
let passed = 0, failed = 0;
for (const { name, fn } of tests) {
  try { fn(); passed++; console.log('  ✓ ' + name); }
  catch (e) { failed++; console.error('  ✗ ' + name + '\n    ' + e.message); }
}
console.log(`\n${passed} 项通过, ${failed} 项失败`);
process.exit(failed ? 1 : 0);
