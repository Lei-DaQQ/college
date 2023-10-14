'''
Author: Jx L li.junxian@outlook.com
Date: 2023-10-07 17:28:44
LastEditors: Jx L li.junxian@outlook.com
LastEditTime: 2023-10-07 17:32:25
FilePath: /college_root/college/2023aut-y2s/zuiyouhua/dong.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 定义目标函数
def target_function(x):
    return x**3 - 2*x + 1
# 初始搜索范围
a = 0
b = 3
epsilon = 0.05
# 打印表头
print("k    a        b          lambda     mu       f(lambda)   f(mu)")
k = 0
while (b - a) >= epsilon:
    lambda_ = a + (b - a) * 0.382  # 黄金分割点
    mu = a + (b - a) * 0.618      # 黄金分割点
    
    f_lambda = target_function(lambda_)
    f_mu = target_function(mu)
    
    # 打印迭代结果
    print(f"{k}    {a:.4f}   {b:.4f}   {lambda_:.4f}    {mu:.4f}    {f_lambda:.4f}   {f_mu:.4f}")
    
    if f_lambda < f_mu:
        b = mu
    else:
        a = lambda_
    
    k += 1
# 输出最终结果
x_optimal = (a + b) / 2
min_value = target_function(x_optimal)
print(f"\n最优解: x = {x_optimal:.4f}, 最小值: {min_value:.4f}")