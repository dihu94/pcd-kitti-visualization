import open3d as o3d
import numpy as np
import os
import sys
import math 

from decimal import Decimal, ROUND_HALF_UP

if __name__ == "__main__":
    dirname = "0715/"
    dirs = os.listdir(dirname)
    print("There are " + str(len(dirs)) + " Lidar objects in the directory")
    for index, file in enumerate(dirs):
        pcdname = file
        pcd_timestamps = pcdname.split('.') 
        filename = dirname  + pcdname
        
        pcd = o3d.io.read_point_cloud(filename)
        pcd_load = np.asarray(pcd.points)

        
        pcd_nanosec = pcd_timestamps[1][:2]
        bag_secs = int(pcd_timestamps[0])

        bag_nsecs = Decimal(float(pcd_timestamps[1][:2])/10.0).quantize(0, ROUND_HALF_UP)

        if (bag_nsecs == 10):
            bag_secs += 1
            bag_nsecs = 0

        numpy_filename = "0715_numpy/" + str(bag_secs) + '.'+ str(bag_nsecs)
        np.save(numpy_filename, pcd_load)
        print(index)
        percentage = math.ceil(float(index)/float(len(dirs))*1000.0)/10.0
        print ("Conversion is at " + str(percentage) +"%")

        
    

