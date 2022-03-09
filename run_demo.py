# !/usr/bin/python3
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
plt.rc('font',family='Times New Roman')

np.random.seed(19961110)

# 初始参数
n = 28
r_c = 4
i_location = np.array([0, 0])
x_locations = np.random.uniform(i_location[0] - r_c, i_location[0] + r_c, n)
y_locations = np.random.uniform(i_location[1] - r_c, i_location[1] + r_c, n)
locations = np.column_stack((x_locations, y_locations))

# 找到邻居
# 旋转359°，记录下每次旋转后
# 4个扇区中智能体的个数ns = [n1,n2,n3,n4]，计算VAR(ns)
# 统计所有VAR(ns)，
def rotate_sector(one_rotate_deg, base_vec):
    one_rotate_rad = np.deg2rad(one_rotate_deg)
    # 旋转后的基准向量
    one_rotate_base_vec = np.array([
        base_vec[0] * np.cos(one_rotate_rad) - base_vec[1] * np.sin(one_rotate_rad),
        base_vec[0] * np.sin(one_rotate_rad) + base_vec[1] * np.cos(one_rotate_rad)
    ])

    # # 旋转后的扇区范围
    # one_rotate_sec_ranges = base_sector_ranges + one_rotate_deg
    # change_idx = np.where(one_rotate_sec_ranges > 360)
    # one_rotate_sec_ranges[change_idx] = one_rotate_sec_ranges[change_idx] - 360
    return one_rotate_base_vec

def which_sector(sec_ranges, one_rotate_base_vec, ij_vector, rotate_deg):
    # 邻居j所在i扇区分布内的第几个扇区
    # 算出
    dot = one_rotate_base_vec.dot(ij_vector)  # dot product between [x1, y1] and [x2, y2]
    det = one_rotate_base_vec[0] * ij_vector[1] - one_rotate_base_vec[1] * ij_vector[0]  # determinant
    one_rad = np.arctan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    one_deg = np.rad2deg(one_rad)   # 这个算出来的范围是1,2象限0-180, 3,4象限-180-0°
    # 转换为0-360范围
    if one_deg < 0:
        one_deg = 360 + one_deg
    # 加上旋转角
    # one_deg += rotate_deg
    #
    one_sec = 3

    for i in range(4):
        if one_deg > sec_ranges[i]:
            one_sec = i
    # print(one_deg, sec_ranges, one_sec)

    return one_deg, one_sec

delta_rotate = 1
base_sector_ranges = np.array([0, 90, 180, 270])
rotate_degs = []    # 旋转角度列表
vars = []           # 每个扇区个数的方差列表
for one_rotate_deg in range(0, 90, delta_rotate):
    # 基准向量
    base_vec = np.array([10, 0])
    base_vec_v = np.array([0, 10])
    # 旋转后的扇区区间范围，旋转后的基准向量
    one_rotate_base_vec = rotate_sector(one_rotate_deg, base_vec)
    one_rotate_base_vec_v = rotate_sector(one_rotate_deg, base_vec_v)

    ax = plt.subplot(111)

    # 感知半径圆
    patch = Circle(i_location, radius=r_c, fill=False)
    ax.add_patch(patch)
    # 智能体点
    ax.scatter(i_location[0], i_location[1], s=120, c="red")
    ax.scatter(locations[:, 0], locations[:, 1], s=120, c='white',edgecolor='k')

    ax.plot(
        [i_location[0]-one_rotate_base_vec[0], i_location[0]+one_rotate_base_vec[0]], [i_location[1]-one_rotate_base_vec[1], i_location[1]+one_rotate_base_vec[1]]
    )
    ax.plot(
        [i_location[0]-one_rotate_base_vec_v[0], i_location[0]+one_rotate_base_vec_v[0]], [i_location[1]-one_rotate_base_vec_v[1], i_location[1]+one_rotate_base_vec_v[1]]
    )

    #
    sec_num = [0, 0, 0, 0]  # 0,1,2,3扇区中邻居数量
    for i in range(len(locations)):
        one_location = locations[i]
        one_dis = np.linalg.norm(one_location - i_location)
        ij_vector = one_location - i_location  # 邻居j与i组成的向量
        # 只有在感知半径以内的智能体才需要计算扇区
        if one_dis <= r_c:
            one_deg, one_sec = which_sector(base_sector_ranges, one_rotate_base_vec, ij_vector, one_rotate_deg)
            ax.annotate(f"{one_sec}", one_location + np.array([-0.08, -0.12]))
            sec_num[one_sec] += 1

        # ax.annotate("{:.2f}".format(one_deg), one_location+np.array([0.1, 0.1]))

        # 样式
        ax.set_xlim([i_location[0] - r_c, i_location[0] + r_c])
        ax.set_ylim([i_location[1] - r_c, i_location[1] + r_c])
        ax.set_aspect(1./ax.get_data_ratio())
    vars.append(np.var(sec_num))
    rotate_degs.append(one_rotate_deg)

    ax.text(5, 2, f"{sec_num}", size=10, rotation=0.,
             ha="center", va="center",
             bbox=dict(boxstyle="round",
                       ec=(1., 0.5, 0.5),
                       fc=(1., 0.8, 0.8),
                       )
             )
    ax.text(5, 1, f"VAR: {np.var(sec_num)}", size=10, rotation=0.,
            ha="center", va="center",
            bbox=dict(boxstyle="round",
                      ec=(1., 0.5, 0.5),
                      fc=(1., 0.8, 0.8),
                      )
            )
    print(one_rotate_deg, sec_num, np.var(sec_num))
    # plt.show()
    plt.savefig(f"./example/{one_rotate_deg}.png")
    plt.close('all')
min_idx = np.argmin(vars)
min_deg = rotate_degs[min_idx]
print(min_deg)
