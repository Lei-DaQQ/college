import numpy as np
import matplotlib.pyplot as plt

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

    epsilon = 1e-3

    x_arr, f_arr = [], []

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

        x_arr.append(list(x0))

        f_arr.append(fun(x0))

        k += 1

    return x0, fun(x0), x_arr, f_arr  # 分别是最优点坐标，最优值，迭代次数


def main():
    x0 = [-1.9, 2]  # 初始点
    # x0 = np.array([0, 0])

    x, fx, xiter, fiter = steepest_descent_method(fun, gfun, x0)

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

    ax.set_title("Steepest Descent for Rosbrock")

    ax = fig.add_subplot(1, 2, 2)

    ax.plot(fiter)

    ax.set_title(
        "Banana Function, Steepest Descent迭代过程",
        {"fontname": "STFangsong", "fontsize": 12},
    )

    ax.set_xlabel("迭代次数", {"fontname": "STFangsong", "fontsize": 12})
    plt.show()


if __name__ == "__main__":
    main()
