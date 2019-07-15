import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from itertools import chain
from Tkinter import *
from tkFileDialog   import askopenfilename   

file_path_string = askopenfilename()

print("**********************************************")
print("Import the point cloud data saved in npy file " + str(file_path_string)) 
fileformat = ".npy"
data = np.load(file_path_string )


label_file_path_string = askopenfilename()
label_file = open(label_file_path_string, "r")
label_lines = label_file.read()
label_lines = label_lines.split("\n")

if (len(label_lines)> 0):
    print("file is valid " + str(len(label_lines)) + " " + label_file_path_string)
    object_to_draw = []
    for index, label_lines in enumerate(label_lines):
        label_segment = label_lines.split()
        if (len(label_segment)> 0):
            typeObject = label_segment[0]
            h =  float(label_segment[8])
            d  =  float(label_segment[9])
            l =  float(label_segment[10])
            y =  float(label_segment[11]) * (-1.0)
            z =  float(label_segment[12])
            x =  float(label_segment[13]) -0.5
            w =  float(label_segment[14])  


            points = [[x-l/2.0, y-d/2.0, z-h/2.0], [x+l/2.0, y-d/2.0, z-h/2.0], [x-l/2.0, y+d/2.0, z-h/2.0], [x+l/2.0, y+d/2.0, z-h/2.0],
            [x-l/2.0, y-d/2.0, z+h/2.0], [x+l/2.0, y-d/2.0, z+h/2.0], [x-l/2.0, y+d/2.0, z+h/2.0], [x+l/2.0, y+d/2.0, z+h/2.0]]
            lines = [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5], [4, 6], [5, 7], [6, 7],
                        [0, 4], [1, 5], [2, 6], [3, 7]]
            colors = [[1, 0, 0] for i in range(len(lines))]
            line_set = o3d.geometry.LineSet()
            line_set.points = o3d.utility.Vector3dVector(points)
            line_set.lines = o3d.utility.Vector2iVector(lines)
            line_set.colors = o3d.utility.Vector3dVector(colors)
            object_to_draw.append(line_set)
                
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(data)

object_to_draw.append(pcd)
o3d.visualization.draw_geometries(object_to_draw)

print("**********************************************")
print("add one row")
append_data=np.append(data, [1])
print(append_data)
