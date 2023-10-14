"""
Author: ljx li.junxian@outlook.com
Date: 2023-10-13 14:39:53
LastEditors: ljx li.junxian@outlook.com
LastEditTime: 2023-10-13 14:43:31
FilePath: \zuiyouhua\06_最速_牛顿法\newton.py
Description: 

Copyright (c) 2023 by Jx L, All Rights Reserved. 
"""

import numpy as np

import matplotlib.pyplot as plt

##1. 定义函数、梯度、hessian矩阵

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




def Newton(fun, gfun, hess, x0):
    # 功能：用Newton算法求解无约束问题：min fun(x)

    # 输入：x0是初始点，fun,gfun分别是目标函数和梯度

    # 输出：x,val分别是近似最优点和最优解,k是迭代次数

    maxk, rho, sigma, epsilon = 1e4, 0.55, 0.4, 1e-3

    k = 0

    n = np.shape(x0)[0]

    # 海森矩阵可以初始化为单位矩阵

    Gk = np.eye(n)  # np.linalg.inv(hess(x0)) #或者单位矩阵np.eye(n)

    x_arr, f_arr = [x0], []

    while k < maxk:
        gk = gfun(x0)

        Gk = hess(x0)

        if np.linalg.norm(gk) < epsilon:
            break

        try:
            dk = -1.0 * (np.linalg.inv(Gk) @ gk)

        except:
            print("Gk is sigular! Fail to continue")

            break

        m, mk = 0, 0

        while m < 20:  # 用Armijo搜索求步长
            if fun(x0 + rho**m * dk) < fun(x0) + sigma * rho**m * np.dot(gk, dk):
                mk = m

                break

            m += 1

        # Newton迭代

        x = x0 + rho**mk * dk

        k += 1

        x0 = x

        x_arr.append(list(x0))

        f_arr.append(fun(x0))

    return x0, fun(x0), x_arr, f_arr  # 分别是最优点坐标，最优值，迭代次数


def main():
    x0 = [-1.9, 2]  # 初始点

    x, fx, xiter, fiter = Newton(fun, gfun, hess, x0)

    fig = plt.figure(figsize=(8, 3))

    # Contour plot

    x = np.linspace(-2, 2, 50)

    y = np.linspace(-0.7, 3.3, 50)

    X, Y = np.meshgrid(x, y)

    Z = fun([X, Y])

    ax = fig.add_subplot(1, 2, 1)

    ax.contour(X, Y, Z, 60, cmap="jet")

    xiter = np.matrix(list(xiter))

    ax.plot(xiter[:, 0], xiter[:, 1], "-.")

    # ax.quiver(iter_x[:-1], iter_y[:-1], anglesx, anglesy, scale_units = 'xy', angles = 'xy', scale = 1, color = 'r', alpha = .3)

    ax.set_title("Newton for Rosbrock")

    ax = fig.add_subplot(1, 2, 2)

    ax.plot(fiter)

    ax.set_title(
        "Banana Function, Newton迭代过程", {"fontname": "STFangsong", "fontsize": 12}
    )

    ax.set_xlabel("迭代次数", {"fontname": "STFangsong", "fontsize": 12})

    ax.set_ylabel("$f(x)$", {"fontname": "STFangsong", "fontsize": 12})

    plt.show()


if __name__ == "__main__":
    main()
