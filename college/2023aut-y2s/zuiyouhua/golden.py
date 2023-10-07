'''
Author: Jx L li.junxian@outlook.com
Date: 2023-10-07 17:05:38
LastEditors: Jx L li.junxian@outlook.com
LastEditTime: 2023-10-07 17:37:33
FilePath: /college_root/college/2023aut-y2s/zuiyouhua/golden.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import math

def golden_section_optimization(f, a, b, epsilon):
    k = 0
    lambda_ = a + (3 - math.sqrt(5)) * (b - a) / 2
    mu = a + b - lambda_
    f_lambda = f(lambda_)
    f_mu = f(mu)

    print("k    a          b          lambda    mu        f(lambda)    f(mu)")
    print(f"{k}    {a:.4f}    {b:.4f}    {lambda_:.4f}    {mu:.4f}    {f_lambda:.4f}    {f_mu:.4f}")

    while abs(b - a) > epsilon:
        if f_lambda < f_mu:
            b = mu
            mu = lambda_
            lambda_ = a + b - mu
            f_mu = f_lambda
            f_lambda = f(lambda_)
        else:
            a = lambda_
            lambda_ = mu
            mu = a + b - lambda_
            f_lambda = f_mu
            f_mu = f(mu)

        k += 1
        print(f"{k}    {a:.4f}    {b:.4f}    {lambda_:.4f}    {mu:.4f}    {f_lambda:.4f}    {f_mu:.4f}")

    return (a + b) / 2

# 
def f(x):
    return x**3 - 2*x + 1

a = 0
b = 3
epsilon = 0.05

result = golden_section_optimization(f, a, b, epsilon)
print(f"Optimal solution: {result:.4f}")
print(f"target value: {f(result):.4f}")
