import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from itertools import chain
from tkinter import filedialog





print("**********************************************")
print("Import the KITTI point cloud data saved in npy file")
kitti_data = np.fromfile('1561494153.4.npy', dtype=np.float32).reshape(-1, 4)
n = 4 #separate kitti list
kitti_cache = kitti_data
print(kitti_cache)

print("**********************************************")
print("Cast them to multiple npy scalars")

kitti_cache=np.delete(kitti_cache, 3,1)
np.save("kitti_cache.npy", kitti_cache)
print(kitti_cache)


print("**********************************************")
print("Convert to npy")
kitti_split = np.load('kitti_cache.npy')
kitti_split = np.asarray(kitti_split)
print(kitti_split)

kitti_pcd = o3d.geometry.PointCloud()
kitti_pcd.points = o3d.utility.Vector3dVector(kitti_cache)
print(kitti_pcd)
o3d.visualization.draw_geometries([kitti_pcd])

