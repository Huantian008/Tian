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
mileage_col = '拥堵公里'

top10 = df.sort_values(by=bar_col, ascending=False).head(10).reset_index(drop=True)

x = top10['地区']
y1 = top10[bar_col]
y2 = top10[line_col]

fig, ax1 = plt.subplots(figsize=(12, 7))

bars = ax1.bar(
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

ax2.plot(
    x,
    y2,
    color='red',
    marker='o',
    linewidth=2,
    markersize=6,
    label='平均速度(km/h)'
)

ax2.set_ylabel('平均速度(km/h)', fontsize=13)

info_text = ax1.text(
    0.02,
    0.96,
    '',
    transform=ax1.transAxes,
    ha='left',
    va='top',
    fontsize=12,
    bbox=dict(boxstyle='round,pad=0.35', fc='#eef7e8', ec='#666666', alpha=0.9)
)
info_text.set_visible(False)


def show_mileage(index):
    row = top10.iloc[index]
    info_text.set_text(
        f"{row['地区']}\n"
        f"拥堵里程：{row[mileage_col]:.2f} 公里"
    )
    info_text.set_visible(True)

    for bar in bars:
        bar.set_color('skyblue')
    bars[index].set_color('#66b9d9')

    fig.canvas.draw_idle()


def on_click(event):
    for index, bar in enumerate(bars):
        contains, _ = bar.contains(event)
        if contains:
            show_mileage(index)
            break


fig.canvas.mpl_connect('button_press_event', on_click)

plt.title('南昌各区域拥堵指数与平均速度关联对比', fontsize=16, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig(base_dir / '南昌行政区域拥堵情况Top10_点击柱状图.png', dpi=300)
plt.show()
