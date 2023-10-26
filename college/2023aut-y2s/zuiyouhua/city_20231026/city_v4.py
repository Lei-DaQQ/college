
import numpy as np
from scipy.optimize import minimize

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from matplotlib.font_manager import FontProperties
from matplotlib.animation import FuncAnimation
import imageio

def check_symmetry(matrix):
    # 检查矩阵是否对称
    is_symmetric = np.allclose(matrix, matrix.T, atol=1e-8)

    # 找到所有不对称的位置
    if not is_symmetric:
        non_symmetric_positions = np.where(matrix != matrix.T)
    else:
        non_symmetric_positions = None

    if is_symmetric:
        print("矩阵是对称的。")
    else:
        print("矩阵不是对称的。")
        print("不对称的位置：")
        for row, col in zip(*non_symmetric_positions):
            print(f"行 {row}, 列 {col}, 元素 {matrix[row][col]}")

def fix_asymmetry(matrix):
    # 找到不对称的位置
    non_symmetric_positions = np.where(matrix != matrix.T)
    
    # 修复不对称的元素
    for row, col in zip(*non_symmetric_positions):
        if abs(matrix[row, col]) > abs(matrix[col, row]):
            matrix[row, col] = matrix[row, col]
        else:
            matrix[row, col] = matrix[col, row]
    
    return matrix

def read_distance_matrix_from_csv(file_path):
    # 从CSV文件读取数据，使用制表符作为分隔符
    data = pd.read_csv(file_path, sep=',', header=0, index_col=0)

    # 将数据转换为NumPy数组
    distance_matrix = data.to_numpy()

    # 获取城市名称
    city_names = data.index

    return distance_matrix, city_names

def visualize_cities(distance_matrix, city_names, city_positions):

    # 设置字体和启用汉字支持
    font_properties = FontProperties(fname='SimHei.ttf')  # 替换为包含汉字的TTF字体文件路径
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 替换为你的TTF字体名称
    plt.rcParams['axes.unicode_minus'] = False  # 处理坐标轴负号显示问题

    # 可视化结果
    plt.figure(figsize=(8, 6))
    plt.scatter(city_positions[:, 0], -city_positions[:, 1])

    # 在图上添加城市名称
    for i, (x, y) in enumerate(city_positions):
        plt.text(x, -y, city_names[i], fontsize=8, fontproperties=font_properties)

    plt.title('City Map Using conjugate gradient')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()




# 定义目标函数，即要最小化的函数
def objective_function(city_coordinates, actual_distances):

    num_cities = city_coordinates.shape[0] // 2
    loss = 0
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            x_i, y_i = city_coordinates[2*i], city_coordinates[2*i+1]
            x_j, y_j = city_coordinates[2*j], city_coordinates[2*j+1]
            distance_ij = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
            loss += (distance_ij**2 - actual_distances[i, j]**2)**2

    return loss

def callback_function(xk):
    # xk 包含了当前迭代的结果
    # 在这里你可以保存 xk 或者进行其他处理
    results.append(xk)


def update(frame):
    # 设置字体和启用汉字支持
    font_properties = FontProperties(fname='SimHei.ttf')  # 替换为包含汉字的TTF字体文件路径
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 替换为你的TTF字体名称
    plt.rcParams['axes.unicode_minus'] = False  # 处理坐标轴负号显示问题

    # 获取当前迭代的城市坐标
    # current_coordinates = results[frame]
    current_coordinates = results[frame].reshape(-1, 2)

    # 在图上添加城市名称前，清除之前的文本对象
    for text in ax.texts:
        text.remove()

    # for line in ax.lines:
    #         line.remove()

    # 定义不同城市和轨迹的颜色
    city_colors = global_city_colors
    track_colors = city_colors

# 哈尔滨在4下标， 长春在5坐标，保证哈尔滨的x y 都比 长春大
    # 绘制城市的轨迹
    for i in range(len(current_coordinates)):
        x, y = current_coordinates[i]
        city_color = city_colors[i]
        track_color = track_colors[i]
        # ax.scatter(x, -y, color=city_color, s=50)  # 绘制城市
        # ax.text(x, y, city_names[i], fontsize=8, fontproperties=font_properties)
        
        # 绘制轨迹线段
        if frame > 0:
            previous_coordinates = results[frame - 1].reshape(-1, 2)
            x_values = [previous_coordinates[i, 0], x]
            y_values = [previous_coordinates[i, 1], y]
            ax.plot(x_values, y_values, color=track_color, linewidth=3, linestyle='-', alpha=0.2)


    # 更新散点图的数据
    sc.set_offsets(np.c_[current_coordinates[:, 0], current_coordinates[:, 1]])
    
    # 在图上添加城市名称
    for i, (x, y) in enumerate(current_coordinates):
        ax.text(x, y, city_names[i], fontsize=8, fontproperties=font_properties)
    # 更新标题，显示迭代次数
    ax.set_title(f'Iteration {frame+1}')


    # plt.title('City Map Using conjugate gradient')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    # plt.grid(True)
    # plt.show()


def methods(method_name):
    return minimize(objective_function, city_coordinates, method=method_name, args=(actual_distances),callback=callback_function)


def trans(optimal):
    global results
    ha = 4
    wu = 16

    # results = [[res.reshape(-1, 2)] for res in results]
    # print(results)


    if(optimal[ha][0] < 0):
        optimal = [[-x,y] for x,y in optimal]
        results = [ [-elem if index % 2 == 0 else elem for index, elem in enumerate(res) ] for res in results]

    if(optimal[ha][1] < 0):
        optimal = [[x,-y] for x,y in optimal]
        results = [ [-elem if index % 2 == 1 else elem for index, elem in enumerate(res) ] for res in results]



    if(optimal[wu][0] > 0):
        optimal = [[y,x] for x,y in optimal]
        for index, my_list in  enumerate(results):
            for i in range(0, len(my_list)-1, 2):
                my_list[i], my_list[i+1] = my_list[i+1], my_list[i]
            results[index] = my_list

    results = np.array(results)


    print(results)



def main():
    global city_names, global_city_colors
    global results, city_coordinates, actual_distances
    global fig, ax, sc


    global_city_colors = [
        "red", "green", "blue", "yellow", "purple", "orange", "pink", "brown",
        "gray", "cyan", "magenta", "olive", "teal", "indigo", "violet", "beige",
        "lavender", "maroon", "navy", "turquoise", "gold", "silver",
        "khaki", "sienna", "orchid", "crimson", "salmon", "lime",
        "skyblue", "slategray", "peru", "plum", "darkgreen", "dodgerblue"
    ]

    # 调用函数并传入CSV文件路径
    file_path = 'city.csv'  # 替换为你的CSV文件路径
    distance_matrix, city_names = read_distance_matrix_from_csv(file_path)

    # print(distance_matrix)
    # check_symmetry(distance_matrix)
    fix_asymmetry(distance_matrix)

    # 假设的城市坐标（初始值），这里使用随机值作为初始值
    num_cities = 34
    city_coordinates = np.random.uniform(low=-2000, high=2000, size=(num_cities, 2)) 
    # haerbin = city_names.index('哈尔滨')
    # haerbin = 4
    # city_coordinates[haerbin]=[3000,3000]
    # 实际城市之间的距离矩阵（根据你的数据）
    actual_distances = distance_matrix


    methods_list=["CG", "Nelder-Mead", "BFGS"]
    # 初始化结果列表
    results = []
    # 使用Scipy的 minimize 函数来最小化目标函数
    result = methods(methods_list[0]) 


    # 最优的城市坐标
    optimal_city_coordinates = result.x

    optimal_city_coordinates = optimal_city_coordinates.reshape(-1, 2)
    trans(optimal_city_coordinates)

    fig, ax = plt.subplots()
    ax.set_xlim(-2500, 2500)
    ax.set_ylim(-2500, 2500)

    sc = ax.scatter(city_coordinates[:, 0], city_coordinates[:, 1],  color = global_city_colors)

    
    ani = FuncAnimation(fig, update, frames=len(results), repeat=False, interval=500)


    # 文件名和路径，根据需要修改
    # output_filename = 'city_animation.gif'

    # # 保存动画为 GIF 图像
    # with imageio.get_writer(output_filename, mode='I', duration=1) as writer:
    #     for i in range(len(results)):
    #         update(i)  # 更新图像
    #         fig.canvas.draw()
    #         image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    #         image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    #         writer.append_data(image)


    # 显示动画
    plt.show()


    # 调用函数并传入距离矩阵和城市名称
    # visualize_cities(distance_matrix, city_names, optimal_city_coordinates)


if __name__ == '__main__':
    main()