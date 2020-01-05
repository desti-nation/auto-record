# import numpy as np
import cv2
# import argparse
import os
import datetime
import time
import sys
# python record_video_for_exe.py 1 ./video 720 30 1 10 10
# --camera_id --save_root --resolution --fps --show --record_seconds --sleep_seconds


def resolution_to_hw(reso):
    dic = {1080:(1920, 1080), 720:(1280,720)}
    if reso in [1080, 720]:
        return dic[reso]
    else:
        print("Error: Resolution Error.")
        exit()

def check_path(path):
    if not os.path.isdir(path): os.makedirs(path)


if __name__ == "__main__":
    camera_id= int(sys.argv[1])
    save_root = str(sys.argv[2])
    resolution = int(sys.argv[3])
    fps = int(sys.argv[4])
    show = int(sys.argv[5])
    record_seconds = int(sys.argv[6])
    sleep_seconds = int(sys.argv[7])


    print("camera_id = {}, save_root = {}, resolution = {}, fps = {}, show = {}, record_seconds = {}, sleep_seconds = {}".\
    format(camera_id, save_root, resolution, fps, show, record_seconds, sleep_seconds))

    width, height = resolution_to_hw(resolution)
    print("Record height = {}, width = {}".format(height, width))
    check_path(save_root)

    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_count = 0
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    # fourcc = cv2.VideoWriter_fourcc(*'MPEG')

    origintime = datetime.datetime.now()

    while(True):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        save_path = "{}/{}.avi".format(save_root, nowTime)
        out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        
        starttime = datetime.datetime.now()
        print("start record...")
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                # frame = cv2.flip(frame,0)
                # write the flipped frame
                # if (datetime.datetime.now() - starttime).seconds > 2: # skip first seconds for camera initialization
                out.write(frame)
                
                if show: 
                    cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            if (datetime.datetime.now() - starttime).seconds > record_seconds:
                break
        print(save_path, "saved.\n")
        video_count += 1
        print("This is {} th video".format(video_count))
        time.sleep(sleep_seconds)

        if (datetime.datetime.now() - origintime).seconds > 86400*2:
            break
    
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Finish")

    
