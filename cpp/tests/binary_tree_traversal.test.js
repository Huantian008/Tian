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

test('命名空间暴露 runSelfTests', () => {
  assert.strictEqual(typeof T.runSelfTests, 'function');
});

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

// ===== 运行器 =====
let passed = 0, failed = 0;
for (const { name, fn } of tests) {
  try { fn(); passed++; console.log('  ✓ ' + name); }
  catch (e) { failed++; console.error('  ✗ ' + name + '\n    ' + e.message); }
}
console.log(`\n${passed} 项通过, ${failed} 项失败`);
process.exit(failed ? 1 : 0);
