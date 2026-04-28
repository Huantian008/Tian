from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

base_dir = Path(__file__).resolve().parent
file_path = base_dir / '南昌行政区域拥堵情况.xlsx'

df = pd.read_excel(file_path, sheet_name='Sheet1')
df = df.dropna()

bar_col = '高峰'
line_col = '平均速度'

top10 = df.sort_values(by=bar_col, ascending=False).head(10).reset_index(drop=True)

x = top10['地区']
y1 = top10[bar_col]
y2 = top10[line_col]

fig, ax1 = plt.subplots(figsize=(12, 7))

ax1.bar(
    x,
    y1,
    color='skyblue',
    width=0.8,
    label='拥堵指数'
)

ax1.set_xlabel('地区', fontsize=13)
ax1.set_ylabel('拥堵指数', fontsize=13)
ax1.tick_params(axis='x', rotation=45)
ax1.set_ylim(0, y1.max() + 0.3)

ax2 = ax1.twinx()

line, = ax2.plot(
    x,
    y2,
    color='red',
    marker='o',
    linewidth=2,
    markersize=6,
    label='平均速度(km/h)'
)

ax2.set_ylabel('平均速度(km/h)', fontsize=13)

annotation = ax2.annotate(
    '',
    xy=(0, 0),
    xytext=(-70, 20),
    textcoords='offset points',
    bbox=dict(boxstyle='round,pad=0.4', fc='#ffff80', ec='#777777', alpha=0.9),
    arrowprops=dict(arrowstyle='->', color='#555555')
)
annotation.set_visible(False)


def update_annotation(index):
    row = top10.iloc[index]
    annotation.xy = (row['地区'], row[line_col])
    annotation.set_text(
        f"地区：{row['地区']}\n"
        f"平均速度：{row[line_col]:.2f} km/h"
    )


def on_mouse_move(event):
    visible = annotation.get_visible()

    if event.inaxes == ax2:
        contains, info = line.contains(event)
        if contains:
            point_index = info['ind'][0]
            update_annotation(point_index)
            annotation.set_visible(True)
            fig.canvas.draw_idle()
            return

    if visible:
        annotation.set_visible(False)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

plt.title('南昌各区域拥堵指数与平均速度关联对比', fontsize=16, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig(base_dir / '南昌行政区域拥堵情况Top10_交互提示.png', dpi=300)
plt.show()
