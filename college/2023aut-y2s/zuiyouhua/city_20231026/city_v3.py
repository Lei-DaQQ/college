# 使用 conjugate gradient，可以得到正确结果，但是方向可能不对，与随机初始的位置坐标有关
import numpy as np
from scipy.optimize import minimize

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from matplotlib.font_manager import FontProperties

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
def objective_function(city_coordinates):

    num_cities = city_coordinates.shape[0] // 2
    loss = 0
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            x_i, y_i = city_coordinates[2*i], city_coordinates[2*i+1]
            x_j, y_j = city_coordinates[2*j], city_coordinates[2*j+1]
            distance_ij = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
            loss += (distance_ij**2 - actual_distances[i, j]**2)**2

    return loss




# 调用函数并传入CSV文件路径
file_path = 'city.csv'  # 替换为你的CSV文件路径
distance_matrix, city_names = read_distance_matrix_from_csv(file_path)

# print(distance_matrix)
# check_symmetry(distance_matrix)
fix_asymmetry(distance_matrix)


# 假设的城市坐标（初始值），这里使用随机值作为初始值
num_cities = 34
city_coordinates = np.random.rand(num_cities, 2)
# 实际城市之间的距离矩阵（根据你的数据）
actual_distances = distance_matrix

# 使用Scipy的 minimize 函数来最小化目标函数
result = minimize(objective_function, city_coordinates, method='CG')

# 最优的城市坐标
optimal_city_coordinates = result.x

# 将一维坐标数组重塑为二维形式，每一行包含城市的x坐标和y坐标
optimal_city_coordinates = optimal_city_coordinates.reshape(-1, 2)

# 打印最优城市坐标
print("Optimal City Coordinates:")
print(optimal_city_coordinates)

# 调用函数并传入距离矩阵和城市名称
visualize_cities(distance_matrix, city_names, optimal_city_coordinates)

