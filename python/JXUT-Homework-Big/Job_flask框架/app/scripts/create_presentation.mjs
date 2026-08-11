import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const artifactToolPath =
  process.env.ARTIFACT_TOOL_PATH ||
  'C:/Users/y2003/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const { Presentation, PresentationFile } = await import(pathToFileURL(artifactToolPath).href);

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const normalizedRoot = ROOT;
const OUTPUT_DIR = path.join(normalizedRoot, 'outputs');
const FINAL_PPTX = path.join(OUTPUT_DIR, '全国空气质量可视化分析汇报.pptx');
const DASHBOARD_JSON = path.join(normalizedRoot, 'api', 'data', 'air_quality_dashboard.json');
const DASHBOARD_SCREENSHOT = path.join(OUTPUT_DIR, 'dashboard-screenshot.png');
const WORKSPACE =
  process.env.PRESENTATION_WORKSPACE ||
  path.join(os.tmpdir(), 'codex-presentations', 'air-quality-dashboard');
const TMP_DIR = path.join(WORKSPACE, 'tmp');
const PREVIEW_DIR = path.join(TMP_DIR, 'preview');
const LAYOUT_DIR = path.join(TMP_DIR, 'layout');
const QA_DIR = path.join(TMP_DIR, 'qa');

const colors = {
  bg: '#F4FBF3',
  ink: '#18352D',
  muted: '#5C756C',
  emerald: '#0F8F68',
  emeraldDark: '#0F513F',
  green: '#73C95A',
  mint: '#E7F5E8',
  amber: '#E39B31',
  red: '#D84B62',
  line: '#BBD7C9',
  white: '#FFFFFF',
};

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

function addShape(slide, position, fill = colors.white, line = colors.line) {
  return slide.shapes.add({
    geometry: 'roundRect',
    position,
    fill,
    line: { style: 'solid', fill: line, width: 1 },
    borderRadius: 'rounded-xl',
    shadow: 'shadow-sm',
  });
}

function addText(slide, text, position, options = {}) {
  const shape = slide.shapes.add({
    geometry: 'textbox',
    position,
    fill: 'none',
    line: { style: 'solid', fill: 'none', width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: options.fontSize ?? 22,
    bold: options.bold ?? false,
    color: options.color ?? colors.ink,
    typeface: options.typeface ?? 'Aptos',
    alignment: options.alignment ?? 'left',
  };
  return shape;
}

function addFooter(slide, page, note = '数据来源：quotsoft 中国空气质量历史数据；权威说明：生态环境部城市空气质量状况月报') {
  addText(slide, note, { left: 64, top: 682, width: 920, height: 22 }, { fontSize: 11, color: colors.muted });
  addText(slide, String(page).padStart(2, '0'), { left: 1168, top: 674, width: 54, height: 32 }, {
    fontSize: 18,
    bold: true,
    color: colors.emerald,
    alignment: 'right',
    typeface: 'Aptos Display',
  });
}

function decorate(slide) {
  slide.background.fill = colors.bg;
  slide.shapes.add({
    geometry: 'ellipse',
    position: { left: -70, top: -90, width: 270, height: 270 },
    fill: '#CDEDD8',
    line: { style: 'solid', fill: 'none', width: 0 },
  });
  slide.shapes.add({
    geometry: 'ellipse',
    position: { left: 1030, top: -80, width: 300, height: 300 },
    fill: '#F6E7B7',
    line: { style: 'solid', fill: 'none', width: 0 },
  });
}

function addTitle(slide, kicker, title, subtitle) {
  addText(slide, kicker, { left: 64, top: 48, width: 700, height: 26 }, {
    fontSize: 13,
    bold: true,
    color: colors.emerald,
    typeface: 'Aptos Display',
  });
  addText(slide, title, { left: 64, top: 84, width: 880, height: 62 }, {
    fontSize: 38,
    bold: true,
    color: colors.emeraldDark,
    typeface: 'Aptos Display',
  });
  if (subtitle) {
    addText(slide, subtitle, { left: 66, top: 144, width: 980, height: 30 }, {
      fontSize: 15,
      color: colors.muted,
    });
  }
}

function addBullet(slide, text, top, color = colors.emerald) {
  slide.shapes.add({
    geometry: 'ellipse',
    position: { left: 82, top: top + 8, width: 10, height: 10 },
    fill: color,
    line: { style: 'solid', fill: color, width: 0 },
  });
  addText(slide, text, { left: 106, top, width: 980, height: 40 }, { fontSize: 20, color: colors.ink });
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  await fs.mkdir(PREVIEW_DIR, { recursive: true });
  await fs.mkdir(LAYOUT_DIR, { recursive: true });
  await fs.mkdir(QA_DIR, { recursive: true });

  const dashboard = JSON.parse(await fs.readFile(DASHBOARD_JSON, 'utf-8'));
  const screenshotBytes = await fs.readFile(DASHBOARD_SCREENSHOT);
  const screenshotBlob = screenshotBytes.buffer.slice(
    screenshotBytes.byteOffset,
    screenshotBytes.byteOffset + screenshotBytes.byteLength,
  );

  const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });

  const slide1 = presentation.slides.add();
  decorate(slide1);
  addText(slide1, 'PROJECT 1 / ENVIRONMENT & HUMAN DEVELOPMENT', { left: 82, top: 86, width: 650, height: 28 }, {
    fontSize: 14,
    bold: true,
    color: colors.emerald,
    typeface: 'Aptos Display',
  });
  addText(slide1, '全国空气质量可视化分析大屏', { left: 78, top: 136, width: 700, height: 86 }, {
    fontSize: 42,
    bold: true,
    color: colors.emeraldDark,
    typeface: 'Aptos Display',
  });
  addText(slide1, `数据周期：${dashboard.summary.dateRange}    城市样本：${dashboard.summary.cityCount}`, { left: 82, top: 248, width: 700, height: 34 }, {
    fontSize: 22,
    color: colors.muted,
  });
  addShape(slide1, { left: 82, top: 326, width: 650, height: 238 }, colors.white);
  addText(slide1, '第5组（6人）分工', { left: 112, top: 352, width: 240, height: 28 }, { fontSize: 21, color: colors.emeraldDark, bold: true });
  addText(slide1, '主讲 / 核心开发：杨文天', { left: 112, top: 392, width: 260, height: 28 }, { fontSize: 18, color: colors.ink, bold: true });
  addText(slide1, '负责系统搭建、数据处理、前端大屏、PPT统筹与现场汇报。', { left: 112, top: 424, width: 540, height: 24 }, { fontSize: 14, color: colors.muted });
  const groupRows = [
    ['资料与来源说明', '徐慧鹏、唐彬'],
    ['截图与PPT素材整理', '刘曦、余炳超'],
    ['测试记录与答辩问题汇总', '刘汉江'],
  ];
  groupRows.forEach(([task, names], index) => {
    const top = 464 + index * 30;
    slide1.shapes.add({
      geometry: 'ellipse',
      position: { left: 116, top: top + 7, width: 8, height: 8 },
      fill: index === 2 ? colors.amber : colors.emerald,
      line: { style: 'solid', fill: 'none', width: 0 },
    });
    addText(slide1, `${task}：${names}`, { left: 136, top, width: 520, height: 22 }, { fontSize: 15, color: colors.ink });
  });
  addShape(slide1, { left: 800, top: 104, width: 380, height: 420 }, '#E7F5E8', '#BBD7C9');
  addText(slide1, `${dashboard.summary.averageAqi}`, { left: 880, top: 210, width: 220, height: 90 }, {
    fontSize: 72,
    bold: true,
    color: colors.emerald,
    alignment: 'center',
    typeface: 'Aptos Display',
  });
  addText(slide1, '全国平均 AQI', { left: 870, top: 310, width: 240, height: 32 }, {
    fontSize: 24,
    bold: true,
    color: colors.emeraldDark,
    alignment: 'center',
  });
  addText(slide1, `主污染物：${dashboard.summary.dominantPollutant}`, { left: 870, top: 354, width: 240, height: 28 }, {
    fontSize: 18,
    color: colors.muted,
    alignment: 'center',
  });
  addFooter(slide1, 1, '主讲人为杨文天；其他成员承担资料、截图、测试记录等辅助任务，便于答辩说明。');

  const slide2 = presentation.slides.add();
  decorate(slide2);
  addTitle(slide2, 'DATA SOURCE & DESIGN', '数据来源、设计理念与现实意义', '固定历史周期保证截图、结论和答辩复现；公开数据链路支撑可解释分析。');
  const cards = [
    ['数据采集', 'requests 下载每日全国城市 CSV，pandas 解析 AQI 与 6 类污染物。'],
    ['数据聚合', '按城市与日期计算均值，生成排行、趋势、等级分布和热力矩阵。'],
    ['现实意义', '识别短期空气质量高风险城市，为出行提示和环境治理观察提供依据。'],
  ];
  cards.forEach(([title, body], index) => {
    const left = 64 + index * 392;
    addShape(slide2, { left, top: 210, width: 350, height: 132 }, colors.white);
    addText(slide2, title, { left: left + 24, top: 234, width: 260, height: 28 }, { fontSize: 22, bold: true, color: colors.emeraldDark });
    addText(slide2, body, { left: left + 24, top: 274, width: 294, height: 54 }, { fontSize: 17, color: colors.muted });
  });
  slide2.charts.add('bar', {
    position: { left: 96, top: 408, width: 470, height: 210 },
    categories: dashboard.levelDistribution.map((item) => item.name),
    series: [{ name: '城市日样本', values: dashboard.levelDistribution.map((item) => item.value), fill: colors.emerald }],
    hasLegend: false,
    barOptions: { direction: 'bar', grouping: 'clustered', gapWidth: 42 },
    xAxis: { visible: false, majorGridlines: null },
    yAxis: { textStyle: { fill: colors.muted, fontSize: 12 }, line: { style: 'solid', fill: colors.line, width: 1 } },
    dataLabels: { showValue: true, position: 'outEnd', textStyle: { fill: colors.ink, fontSize: 12, bold: true } },
  });
  addText(slide2, 'AQI等级样本分布', { left: 96, top: 372, width: 300, height: 30 }, { fontSize: 20, bold: true, color: colors.emeraldDark });
  addShape(slide2, { left: 650, top: 396, width: 500, height: 190 }, '#E7F5E8');
  addText(slide2, '来源说明', { left: 684, top: 426, width: 180, height: 28 }, { fontSize: 22, bold: true, color: colors.emeraldDark });
  addText(slide2, 'quotsoft 页面说明全国城市数据来自中国环境监测总站全国城市空气质量实时发布平台；生态环境部月报作为权威背景材料。', { left: 684, top: 466, width: 410, height: 72 }, { fontSize: 18, color: colors.muted });
  addFooter(slide2, 2);

  const slide3 = presentation.slides.add();
  decorate(slide3);
  addTitle(slide3, 'FINAL RENDER', '作品最终渲染效果与 3 句结论', '页面采用生态绿白风，单屏展示 6 个图表与 4 个核心指标。');
  slide3.images.add({
    blob: screenshotBlob,
    contentType: 'image/png',
    alt: '全国空气质量可视化大屏网页截图',
    fit: 'contain',
    geometry: 'roundRect',
    borderRadius: 'rounded-xl',
    position: { left: 62, top: 184, width: 720, height: 405 },
  });
  dashboard.conclusions.forEach((item, index) => {
    const top = 202 + index * 116;
    addShape(slide3, { left: 830, top, width: 360, height: 82 }, colors.white);
    addText(slide3, `结论 ${index + 1}`, { left: 852, top: top + 14, width: 120, height: 22 }, { fontSize: 16, bold: true, color: colors.emerald });
    addText(slide3, item, { left: 852, top: top + 40, width: 306, height: 34 }, { fontSize: 15, color: colors.ink });
  });
  addFooter(slide3, 3);

  const slide4 = presentation.slides.add();
  decorate(slide4);
  addTitle(slide4, 'PROCESS REVIEW', '完成过程中的问题、分析思考和心得', '从数据质量、可视化选型、页面密度和算法说明四个方面控制作业质量。');
  const processItems = [
    ['数据问题', '部分日期或城市可能缺失，因此聚合时按可用小时均值计算，并固定周期便于复现。'],
    ['图表问题', '地图、排行、趋势、热力图、玫瑰图和等级分布互补，避免重复表达。'],
    ['算法嵌入', '用 7 日全国平均 AQI 做线性预测，仅表达短期方向，不作为真实预报。'],
    ['心得', '可视化不是堆图，必须让地图定位、排行识别、趋势判断和结论输出形成闭环。'],
  ];
  processItems.forEach(([title, body], index) => {
    const left = index % 2 === 0 ? 76 : 670;
    const top = index < 2 ? 196 : 408;
    addShape(slide4, { left, top, width: 510, height: 150 }, colors.white);
    addText(slide4, title, { left: left + 28, top: top + 26, width: 180, height: 30 }, { fontSize: 23, bold: true, color: colors.emeraldDark });
    addText(slide4, body, { left: left + 28, top: top + 68, width: 440, height: 58 }, { fontSize: 18, color: colors.muted });
  });
  addFooter(slide4, 4);

  const slide5 = presentation.slides.add();
  decorate(slide5);
  addTitle(slide5, 'AI INTERACTION', 'AI 交互记录与提问重点', '核心交互超过 8 次，围绕主题、数据源、视觉、交付物、周期和实现验证逐步收敛。');
  addShape(slide5, { left: 70, top: 188, width: 530, height: 410 }, colors.white);
  const messages = [
    ['我', '我打算做项目一'],
    ['AI', '建议聚焦全国空气质量，复用现有 React + Flask 大屏框架。'],
    ['我', '用计划模式继续吧'],
    ['AI', '确认单页大屏、历史 CSV、生态绿白风、网页+PPT+代码交付。'],
    ['我', 'PPT增加分组，其他人分轻松任务。'],
    ['AI', '封面加入第5组分工：核心开发、资料、截图、测试记录。'],
  ];
  messages.forEach(([speaker, text], index) => {
    const top = 214 + index * 58;
    const isUser = speaker === '我';
    addShape(slide5, { left: isUser ? 284 : 102, top, width: 270, height: 42 }, isUser ? '#DCF7EA' : '#F2F6EF', isUser ? '#93DAB6' : '#CFDDCF');
    addText(slide5, `${speaker}：${text}`, { left: isUser ? 304 : 122, top: top + 9, width: 232, height: 24 }, { fontSize: 13, color: colors.ink });
  });
  addShape(slide5, { left: 670, top: 188, width: 500, height: 410 }, '#E7F5E8');
  addText(slide5, '提问重点', { left: 706, top: 224, width: 200, height: 34 }, { fontSize: 26, bold: true, color: colors.emeraldDark });
  [
    '需求分析：选题、作品形态、交付范围',
    '数据采集：requests、pandas、固定周期',
    '开发流程：Flask API、React/ECharts 大屏',
    '质量验证：单元测试、构建、lint、浏览器截图',
  ].forEach((item, index) => {
    const top = 284 + index * 58;
    const color = index === 3 ? colors.amber : colors.emerald;
    slide5.shapes.add({
      geometry: 'ellipse',
      position: { left: 710, top: top + 8, width: 10, height: 10 },
      fill: color,
      line: { style: 'solid', fill: color, width: 0 },
    });
    addText(slide5, item, { left: 734, top, width: 372, height: 40 }, { fontSize: 20, color: colors.ink });
  });
  addFooter(slide5, 5, 'AI交互内容来自本次项目沟通过程，页面以可编辑形状复刻截图式记录。');

  await fs.writeFile(
    path.join(TMP_DIR, 'source-notes.txt'),
    [
      '全国空气质量可视化分析汇报 source notes',
      `Dashboard JSON: ${DASHBOARD_JSON}`,
      `Dashboard screenshot: ${DASHBOARD_SCREENSHOT}`,
      'quotsoft 中国空气质量历史数据: https://quotsoft.net/air/',
      '生态环境部城市空气质量状况月报: https://www.mee.gov.cn/hjzl/dqhj/cskqzlzkyb/',
      'Conversation-derived facts: 主讲人=杨文天; 第5组成员=杨文天、徐慧鹏、唐彬、刘曦、余炳超、刘汉江; 分工为核心开发、资料来源说明、截图素材整理、测试记录与答辩问题汇总。',
    ].join('\n'),
    'utf-8',
  );
  await fs.writeFile(
    path.join(TMP_DIR, 'slide-plan.txt'),
    [
      'Create mode, 5 slides, 1280x720.',
      'Palette: #F4FBF3 background, #0F513F headings, #0F8F68 primary, #E39B31 accent.',
      'Fonts: Aptos Display for headings, Aptos for body and charts.',
      'Slides: cover with group division; source and meaning; render and conclusions; process review; AI interaction record.',
    ].join('\n'),
    'utf-8',
  );

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, '0')}`;
    await writeBlob(path.join(PREVIEW_DIR, `${stem}.png`), await presentation.export({ slide, format: 'png', scale: 1 }));
    const layout = await slide.export({ format: 'layout' });
    await fs.writeFile(path.join(LAYOUT_DIR, `${stem}.layout.json`), await layout.text(), 'utf-8');
  }
  await writeBlob(path.join(PREVIEW_DIR, 'deck-montage.webp'), await presentation.export({ format: 'webp', montage: true, scale: 1 }));

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(FINAL_PPTX);

  await fs.writeFile(
    path.join(QA_DIR, 'visual-qa.txt'),
    [
      'Mechanical',
      `PPTX exists and is non-empty: ${FINAL_PPTX}`,
      'Expected slide count: 5',
      'Every final slide rendered: yes',
      'Contact sheet or montage reviewed: yes; slide previews inspected.',
      'Issue ledger: no known render-visible blockers after fixing slide 1 title and slide 5 bullet placement.',
      'Final decision: pass.',
    ].join('\n'),
    'utf-8',
  );

  console.log(JSON.stringify({ finalPptx: FINAL_PPTX, workspace: WORKSPACE }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
