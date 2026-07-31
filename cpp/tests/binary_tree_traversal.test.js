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

// ===== 运行器 =====
let passed = 0, failed = 0;
for (const { name, fn } of tests) {
  try { fn(); passed++; console.log('  ✓ ' + name); }
  catch (e) { failed++; console.error('  ✗ ' + name + '\n    ' + e.message); }
}
console.log(`\n${passed} 项通过, ${failed} 项失败`);
process.exit(failed ? 1 : 0);
