'''
Author: Jx L li.junxian@outlook.com
Date: 2023-10-26 18:23:07
LastEditors: Jx L li.junxian@outlook.com
LastEditTime: 2023-10-26 18:23:10
FilePath: /city_20231026/color.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from PIL import Image

# 打开图像文件
image = Image.open('your_image.jpg')  # 替换成你的图片文件路径

# 获取图像的宽度和高度
width, height = image.size

# 创建一个空字典来存储颜色及其出现的次数
color_count = {}

# 遍历图像的每个像素
for y in range(height):
    for x in range(width):
        # 获取像素的RGB颜色值
        pixel = image.getpixel((x, y))
        color = (pixel[0], pixel[1], pixel[2])

        # 如果颜色已经在字典中，增加其出现次数；否则，将其添加到字典中
        if color in color_count:
            color_count[color] += 1
        else:
            color_count[color] = 1

# 输出颜色及其出现的次数
for color, count in color_count.items():
    print(f"RGB: {color}, 出现次数: {count}")
