'''
Author: ljx li.junxian@outlook.com
Date: 2023-10-13 14:30:44
LastEditors: ljx li.junxian@outlook.com
LastEditTime: 2023-10-13 14:48:30
FilePath: \zuiyouhua\06_最速_牛顿法\steepest.py
Description: 

Copyright (c) 2023 by Jx L, All Rights Reserved. 
'''

import numpy as np


# 最速下降
# 函数表达式fun

fun = lambda x: 100 * (x[0] ** 2 - x[1]) ** 2 + (x[0] - 1) ** 2

# 梯度向量 gfun

gfun = lambda x: np.array(
    [400 * x[0] * (x[0] ** 2 - x[1]) + 2 * (x[0] - 1), -200 * (x[0] ** 2 - x[1])]
)

# 海森矩阵 hess

hess = lambda x: np.array(
    [[1200 * x[0] ** 2 - 400 * x[1] + 2, -400 * x[0]], [-400 * x[0], 200]]
)


def steepest_descent_method(fun, gfun, x0):
    maxk = 1e5

    rho = 0.5  # [0,1]

    sigma = 0.4  # [0,0.5]

    k = 0

    epsilon = 1e-5

    while k < maxk:
        gk = gfun(x0)

        dk = -gk

        if np.linalg.norm(dk) < epsilon:
            break

        m = 0

        mk = 0

        while m < 20:
            if fun(x0 + rho**m * dk) < fun(x0) + sigma * rho**m * np.dot(
                gk, dk
            ):  # 这里应用了非精确步长搜索算法
                mk = k

                break

            m += 1

        x0 = x0 + rho**m * dk

        k += 1

    return x0, fun(x0), k


def main():
    x0, fun0, k = steepest_descent_method(
        fun, gfun, np.array([0, 0])
    )  # 此处x0是行向量，计算时要转成列向量
    print(x0, fun0, k)


if __name__ == "__main__":
    main()
