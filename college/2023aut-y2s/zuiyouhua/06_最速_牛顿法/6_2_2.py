import numpy as np
import matplotlib.pyplot as plt


def f(x):  # Objective function
    x1 = x[0]
    x2 = x[1]
    y = 100 * ((x2 - x1 ** 2) ** 2) + (1 - x1) ** 2
    return y


def num_grad(x, h):  # Calculate gradient
    df = np.zeros(x.size)
    for i in range(x.size):
        x1, x2 = x.copy(), x.copy()
        x1[i] = x[i] - h
        x2[i] = x[i] + h
        y1, y2 = f(x1), f(x2)
        df[i] = (y2 - y1) / (2 * h)
    return df


def num_hess(x, h):  # Calculate Hessian matrix
    hess = np.zeros((x.size, x.size))
    for i in range(x.size):
        x1 = x.copy()
        x1[i] = x[i] - h
        df1 = num_grad(x1, h)
        x2 = x.copy()
        x2[i] = x[i] + h
        df2 = num_grad(x2, h)
        d2f = (df2 - df1) / (2 * h)
        hess[i] = d2f
    return hess


def ff(x, y): 
    z = 100 * (y - x ** 2) ** 2 + (1 - x) ** 2
    return z

def linesearch(x, dk):  # Perform line search
    ak = 1
    for i in range(20):
        newf, oldf = f(x + ak * dk), f(x)
        if newf < oldf:
            return ak
        else:
            ak = ak / 4  # Update step size iteratively; the step size can be changed arbitrarily, as long as newf is smaller than oldf (e.g., ak = ak/2 is also acceptable)
    return ak


def steepest(x):  # Steepest descent method
    epsilon, h, maxiter = 10 ** -3, 10 ** -5, 10 ** 4
    it = []
    fx = []
    xx = np.linspace(-5, 5, 40)
    yy = np.linspace(-10, 10, 40)
    X, Y = np.meshgrid(xx, yy)
    x1_set = []
    x2_set = []
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    # fig, axs = plt.subplots(1, 2)

    axs[0].contour(X, Y, ff(X, Y), 100)

    for iter1 in range(maxiter):
        grad = num_grad(x, h)
        it.append(iter1)
        fx.append(f(x))
        x1_set.append(x[0])
        x2_set.append(x[1])
        if np.linalg.norm(grad) < epsilon:
            print("Iterations for steepest descent method:", iter1 + 1)
            axs[0].scatter(x1_set, x2_set, 5)
            axs[0].plot(x1_set, x2_set, linewidth=0.5)
            axs[0].set_xlabel('x1')
            axs[0].set_ylabel('x2')
            axs[0].set_title('Steepest Descent Method contour map')

            axs[1].plot(it, fx)
            axs[1].set_xlabel('iter')
            axs[1].set_ylabel('f_x')
            axs[1].set_title('Steepest Descent Method Iterative process')

            plt.show()
            return x
        dk = -grad
        ak = linesearch(x, dk)
        x = x + ak * dk
    return x


def newton_function(x):  # Newton's method
    epsilon, h1, h2, maxiter = 10 ** -3, 10 ** -5, 10 ** -5, 10 ** 4
    it = []
    fx = []
    xx = np.linspace(-5, 5, 40)
    yy = np.linspace(-10, 10, 40)
    X, Y = np.meshgrid(xx, yy)
    x1_set = []
    x2_set = []
    # fig, axs = plt.subplots(1, 2)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].contour(X, Y, ff(X, Y), 100)

    for iter1 in range(maxiter):
        grad = num_grad(x, h1)
        it.append(iter1)
        fx.append(f(x))
        x1_set.append(x[0])
        x2_set.append(x[1])
        if np.linalg.norm(grad) < epsilon:

            print("Iterations for Newton's method:", iter1 + 1)
            axs[0].scatter(x1_set, x2_set, 5)
            axs[0].plot(x1_set, x2_set, linewidth=0.5)
            axs[0].set_xlabel('x1')
            axs[0].set_ylabel('x2')
            axs[0].set_title("Newton's Method contour map")

            axs[1].plot(it, fx)
            axs[1].set_xlabel('iter')
            axs[1].set_ylabel('f_x')
            axs[1].set_title("Newton's Method Iterative process")

            plt.show()
            return x
        hess = num_hess(x, h2)
        dk = -np.linalg.solve(hess, grad)
        ak = linesearch(x, dk)
        x = x + ak * dk
    return x



def main():
    # Test the optimization methods
    x0 = np.array([-1.9, 2])  # Initial guess
    x_steepest = steepest(x0)
    x_newton = newton_function(x0)

    print("Optimal solution for steepest descent method:", x_steepest)
    print("solution", f(x_steepest))

    print("Optimal solution for Newton's method:", x_newton)
    print("solution", f(x_newton))


if __name__ == "__main__":
    main()