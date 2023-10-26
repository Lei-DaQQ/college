#不支持中文，并且城市上下颠倒了，使用mds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS


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
            print(f"行 {row}, 列 {col}, 元素{matrix[row][col]}")


def fix_asymmetry(matrix):
    # 找到不对称的位置
    non_symmetric_positions = np.where(matrix != matrix.T)
    
    # 修复不对称的元素
    for row, col in zip(*non_symmetric_positions):
        if matrix[row, col] > matrix[col, row]:
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



def visualize_cities(distance_matrix, city_names):
    # 使用MDS算法进行降维，n_components设置为2表示将城市映射到2维平面
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    city_positions = mds.fit_transform(distance_matrix)

    # 可视化结果
    plt.figure(figsize=(8, 6))
    plt.scatter(city_positions[:, 0], city_positions[:, 1])

    # 在图上添加城市名称
    for i, (x, y) in enumerate(city_positions):
        plt.text(x, y, city_names[i], fontsize=8)

    plt.title('City Map Using MDS')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()










# 调用函数并传入CSV文件路径
file_path = 'city.csv'  # 替换为你的CSV文件路径
distance_matrix, city_names = read_distance_matrix_from_csv(file_path)

print(distance_matrix)
check_symmetry(distance_matrix)
fix_asymmetry(distance_matrix)

# 调用函数并传入距离矩阵
visualize_cities(distance_matrix, city_names)