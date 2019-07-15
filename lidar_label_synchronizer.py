import os
import math
from shutil import copyfile
if __name__ == "__main__":
    lidar_dirname = "lgsvl-numpy-lidar-data/"
    lidar_dirs = dirs = os.listdir(lidar_dirname)
    lidar_dirs = [e[:-4] for e in lidar_dirs]
    #print(lidar_dirs[0])
    
    label_dirname = "lgsvl-labels/2019-07-10-21-56-00/"
    label_dirs = dirs = os.listdir(label_dirname)
    label_dirs = [e[:-4] for e in label_dirs]
    #print(label_dirs[0])
    
    intersections = (set(lidar_dirs).intersection(set(label_dirs)))
    print(intersections)

    item_to_process = len(intersections)
    
    start_index = 0
    num_of_empty_label = 0
    lidar_output_dir_name = "LGSVL/training/velodyne/"
    label_output_dir_name = "LGSVL/training/label_2/"

    for index, item in enumerate(intersections, start = 0):
        if os.path.getsize(label_dirname + item + ".txt") > 0:
            num_name = str(start_index).zfill(6)
            copyfile(lidar_dirname + item + ".npy", lidar_output_dir_name + num_name+ ".npy")
            copyfile(label_dirname + item + ".txt", label_output_dir_name + num_name + ".txt")
            start_index+=1
            percentage = math.ceil(float(index)/float(item_to_process)*1000.0)/10.0
            #print("Processed the " + str(index +1)+ " of the " +str(item_to_process) + " Label and lidar combination.  There are " + str(num_of_empty_label) +" empty labels. ")  
        else:
            num_of_empty_label+= 1
            #print("Processed the " + str(index +1)+ " of the " +str(item_to_process) + " Label and lidar combination.  There are " + str(num_of_empty_label) +" empty labels. This one is invalid. " ) 

