'''
Author: Jx L li.junxian@outlook.com
Date: 2023-10-26 16:25:46
LastEditors: Jx L li.junxian@outlook.com
LastEditTime: 2023-10-26 20:31:05
FilePath: /city_20231026/tmp.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# for j in range(1, 34):
#     print(j)
    
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# # 创建一个空的图形对象
# fig, ax = plt.subplots()

# # 设置图形范围
# ax.set_xlim(0, 10)
# ax.set_ylim(0, 10)

# # 创建一个点对象
# point, = ax.plot([], [], 'ro')

# # 更新点的位置函数
# def update(frame):
#     x = np.random.uniform(0, 10)  # 随机生成 x 坐标
#     y = np.random.uniform(0, 10)  # 随机生成 y 坐标
#     point.set_data([x], [y])  # 更新点的位置
#     return point,

# # 创建动画对象
# animation = FuncAnimation(fig, update, frames=range(100), interval=1000)

# # 显示动画
# plt.show()


# global_city_colors = [
#     "red", "green", "blue", "yellow", "purple", "orange", "pink", "brown",
#     "gray", "cyan", "magenta", "olive", "teal", "indigo", "violet", "beige",
#     "lavender", "maroon", "navy", "turquoise", "gold", "silver",
#     "khaki", "sienna", "orchid", "crimson", "salmon", "lime",
#     "skyblue", "slategray", "peru", "plum", "darkgreen"
# ]
# print(len(global_city_colors))
import numpy as np





results = [
    np.random.uniform(size=(1, 2)),
    np.random.uniform(size=(1, 2))
]



    
optimal = np.random.uniform(size=(1, 2))

print(optimal)
print(results)


optimal = [[-x,y] for x,y in optimal]
# results = [[[-x,y] for x,y in res ] for res in results]
results = [ [[-elem] if index % 2 == 0 else [elem] for index, elem in enumerate(res) ] for res in results]


print(optimal)
print(results)

