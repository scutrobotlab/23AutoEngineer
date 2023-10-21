import numpy as np
from plyfile import PlyData

def calculate_distance(point_i, point_j):
    return np.linalg.norm(point_i - point_j)

def calculate_diameter(points):
    max_distance = 0

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            print("第"+str(i)+"个点")
            distance = calculate_distance(points[i], points[j])
            if distance > max_distance:
                max_distance = distance

    return max_distance

# 读取PLY文件
ply_data = PlyData.read('./obj_05.ply')

# 获取点云数据
x = ply_data['vertex']['x']
y = ply_data['vertex']['y']
z = ply_data['vertex']['z']

# 构建点云坐标数组
points = np.column_stack((x, y, z))

# 计算直径
diameter = calculate_diameter(points)
print("点云直径:", diameter)

