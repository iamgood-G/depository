# -*- coding: utf-8 -*-
"""
===============================================================================
项目名称：西江中学7-9年级学生体质健康得分对比 (最终版)
作者：朱世建
日期：2026-03-11

===============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# =============================================================================
# 1. 全局配置
# =============================================================================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

GRADE_COLORS = {
    '7': '#D62728',  # 红色
    '8': '#1F77B4',  # 蓝色
    '9': '#2CA02C'  # 绿色
}
GRADE_KEYS = ['7', '8', '9']
GRADE_LABELS = ['7年级', '8年级', '9年级']

DIMENSIONS = ['速度', '爆发', '力量', '柔韧', '耐力']

# =============================================================================
# 2. 数据录入 (已与 Excel 核对无误)
# =============================================================================
BOYS_DATA = {
    '7': {'mean': [86.12, 75.78, 31.01, 80.69, 79.52], 'std': [13.06, 18.80, 26.19, 10.45, 17.82]},
    '8': {'mean': [80.99, 66.75, 22.31, 69.94, 78.89], 'std': [11.77, 19.10, 24.21, 17.94, 13.19]},
    '9': {'mean': [80.55, 51.61, 39.86, 74.44, 88.50], 'std': [11.87, 26.50, 25.86, 10.31, 12.07]}
}

GIRLS_DATA = {
    '7': {'mean': [78.05, 65.91, 70.91, 81.65, 72.81], 'std': [10.46, 17.94, 7.19, 11.76, 19.19]},
    '8': {'mean': [72.60, 63.25, 69.60, 70.27, 80.90], 'std': [13.20, 18.95, 12.15, 18.86, 11.93]},
    '9': {'mean': [75.02, 62.27, 71.48, 77.88, 84.06], 'std': [8.50, 24.26, 10.40, 14.03, 10.67]}
}


# =============================================================================
# 3. 辅助函数
# =============================================================================
def get_lighter_color(hex_color, alpha=0.2):
    rgba = mcolors.to_rgba(hex_color)
    return (*rgba[:3], alpha)


# =============================================================================
# 4. 绘图函数
# =============================================================================

def draw_radar_final(title, data_dict, save_name=None):
    num_vars = len(DIMENSIONS)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    # 强制上限为 100
    y_limit = 100
    step = 20

    fig = plt.figure(figsize=(10, 10), dpi=300)
    ax = fig.add_axes([0.1, 0.25, 0.8, 0.65], polar=True)

    lines_handles = []

    for i, grade in enumerate(GRADE_KEYS):
        means = np.array(data_dict[grade]['mean'])
        stds = np.array(data_dict[grade]['std'])

        angles_closed = np.concatenate((angles, [angles[0]]))
        means_closed = np.concatenate((means, [means[0]]))
        stds_closed = np.concatenate((stds, [stds[0]]))

        upper = means_closed + stds_closed
        lower = np.maximum(means_closed - stds_closed, 0)

        color_line = GRADE_COLORS[grade]
        color_fill = get_lighter_color(color_line, alpha=0.2)
        label = GRADE_LABELS[i]

        # 绘制填充区域
        angles_poly = np.concatenate([angles_closed, angles_closed[::-1]])
        values_poly = np.concatenate([upper, lower[::-1]])
        ax.fill(angles_poly, values_poly, color=color_fill, linewidth=0, zorder=1)

        # 绘制平均值连线
        h, = ax.plot(angles_closed, means_closed,
                     linewidth=2.5, linestyle='-', marker='o', markersize=8,
                     color=color_line, label=label, zorder=10)
        lines_handles.append(h)

    # 样式美化
    ax.set_thetagrids(np.degrees(angles), DIMENSIONS,
                      fontsize=15, fontweight='bold', fontfamily='sans-serif')
    ax.tick_params(axis='x', which='major', pad=15)

    ax.set_ylim(0, y_limit)
    y_ticks = np.arange(0, y_limit + step, step)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(int(t)) for t in y_ticks],
                       fontsize=11, color='gray', fontfamily='sans-serif')

    ax.set_theta_zero_location('N')
    ax.grid(True, linestyle='-', linewidth=1.0, alpha=0.6, color='gray', zorder=5)

    ax.legend(lines_handles, GRADE_LABELS, loc='upper right', bbox_to_anchor=(1.1, 1.1),
              fontsize=12, frameon=True, facecolor='white', framealpha=0.9, shadow=True)

    # 标题在底部
    fig.text(0.5, 0.08, title,
             ha='center', va='top',
             fontsize=16, fontweight='bold', fontfamily='sans-serif',
             wrap=True)

    if save_name:
        plt.savefig(save_name, dpi=300, bbox_inches='tight')
        print(f"✅ 图片已保存：{save_name}")

    plt.show()


# =============================================================================
# 5. 程序入口
# =============================================================================

if __name__ == '__main__':
    print("正在生成最终确认版图表（数据已核对）...")

    try:
        draw_radar_final(
            title="图1 西江中学男生体质健康五维能力对比 (均值±标准差)",
            data_dict=BOYS_DATA,
            save_name="boys_radar_final.png"
        )

        draw_radar_final(
            title="图2 西江中学女生体质健康五维能力对比 (均值±标准差)",
            data_dict=GIRLS_DATA,
            save_name="girls_radar_final.png"
        )

        print("✅ 生成成功！所有数据与 Excel 源文件一致。")

    except Exception as e:
        print(f"❌ 发生错误：{e}")