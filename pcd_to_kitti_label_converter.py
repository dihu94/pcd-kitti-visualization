import open3d as o3d
            
import numpy as np
import math

import os

from decimal import Decimal, ROUND_HALF_UP


if __name__ == "__main__":
    
    label_location = "lgsvl-labels/output_0715.txt"
    print("this tool converts from lgsvl ground truth label to kitti label")
    f=open(label_location, "r")
    if f.mode == 'r':
        labeling =f.read()
    xmin = 0
    xmax = 80
    ymin = -40
    ymax = 40
    zmin = -4
    zmax = 1.25

    #create empty array
    labeling_msgs =  labeling.split('---\n') #which is all the bounding box at one single time stamp
    fileNumber = 0
    allCarNumber = 0
    allPedNumber = 0

    invalidFileNumber = 0

    currentFileName = ""
    for index, msg in enumerate(labeling_msgs, start = 0):
    
        readRows = msg.split('detections: ')
        if (len(readRows)>1):

            time_header = readRows[0] 
            detections = readRows[1]
            detection_info = detections.split('- \n')
            time_info = time_header.split('\n')  

            bag_secs = int(time_info[3][-10:])
            bag_nsecs = int(time_info[4][-10:])
            bag_nsecs = Decimal(float(int(str(bag_nsecs)[:2]))/10.0).quantize(0, ROUND_HALF_UP)

            if (bag_nsecs == 10):
                bag_secs += 1
                bag_nsecs = 0
            
            label_string = ""
            num_escape_object = 0
            for obj_index, detect_msg in enumerate(detection_info, start = 0):
                
                num_cars = 0
                num_ped = 0
                fw=open(label_location[:-4]+"/"+ str(bag_secs) + "." + str(bag_nsecs) +".txt", "w")
                currentFileName = fw.name
                detect_msg_rows = detect_msg.split('\n')
                #print(detect_msg_rows)
                if (len(detect_msg_rows)>2):

                    # the position has been Converted from (Right/Up/Forward) to (Forward/Left/Up)
                    x_pos = float(detect_msg_rows[12].split(': ')[1][:5])
                    y_pos = float(detect_msg_rows[13].split(': ')[1][:5]) #should be transformed
                    z_pos = float(detect_msg_rows[14].split(': ')[1][:5])
                    
                    if (x_pos>xmax or x_pos < xmin or y_pos>ymax or y_pos < ymin or z_pos>zmax or z_pos < zmin ):
                        num_escape_object+=1
                    else:
                        w_or = float(detect_msg_rows[19].split(': ')[1][:5])

                        length =  float(detect_msg_rows[21].split(': ')[1][:5])
                        width =  float(detect_msg_rows[22].split(': ')[1][:5])
                        height =  float(detect_msg_rows[23].split(': ')[1][:5])
                        
                        predObject = detect_msg_rows[7].split('"')[1]
                        if (predObject=="car"):  
                            num_cars = num_cars+1
                            label_string= label_string + "Car" 
                            label_string= label_string + " 0.00 0 0 0 0 0 0 " +  str(height) + " " + str(width) + " "\
	                         + str(length)  + " "+str(y_pos*(-1.0))  + " "+ str(z_pos) + " "+ str(x_pos) + " "+ str(w_or) + '\n'
                            fw.write(label_string)   
                        elif (predObject== "pedestrian"):  
                            num_ped= num_ped+1
                            label_string= label_string + "Pedestrian"
                            label_string= label_string + " 0.00 0 0 0 0 0 0 " +  str(height) + " " + str(width) + " "\
	                         + str(length)  + " "+str(y_pos*(-1.0))  + " "+ str(z_pos) + " "+ str(x_pos) + " "+ str(w_or) + '\n'
                            fw.write(label_string)
	                #save to KITTI camera format instead of velodyne format
	                #KITTI Format: 
	                # |type|truncation|occlusion|alpha|bbox|bbox|bbox|bbox|height|width|length|locationx|locationy|locationz|rotation
	                #the xyz coords have to be transformed from lgsvl lidar coord to camera coord
               
                allCarNumber += num_cars
                allPedNumber += num_ped
                fw.close()

            fileNumber = index
            if (num_cars == 0 and num_ped ==0): 
                invalidFileNumber+=1
                print("invalid label" + currentFileName + "Number of invalid files: " +str(invalidFileNumber) )
            
        print("Processed the " + str(index) + "th Label. Got " + str(num_cars) + "cars and " + str(num_ped) + "pedestrians and "+ str(num_escape_object) + "invalid objects. File name is:" + currentFileName +".")    
    f.close()
    print("Procession complete. Got " + str(fileNumber) + " files and " + str(allCarNumber) + " vehicles and " + str(allPedNumber) + " pedestrians in summary. " )    
