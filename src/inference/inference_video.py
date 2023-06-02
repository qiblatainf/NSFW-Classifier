# Impprting Libraries & Packages

import datetime
import time
import cv2
from keras.models import load_model
import numpy as np
from collections import deque
import warnings

warnings.filterwarnings("ignore")

import sys

sys.path.insert(1, "D:/Repos-Sadiq/ml-kit-algo/nsfw-classifier-qib/src/")
print("sys path = " ,sys.path)

import config
import argparse

vid_model = load_model(config.MODEL_PATH)

labels = {0: "Drawing", 1: "Hentai", 2: "Neutral", 3: "Porn", 4: "Sexy"}
size = 128
Q = deque(maxlen=size)



def predict(file_path):
    
 #   print(file_path)
    vs = cv2.VideoCapture(file_path)
    time.sleep(1)
    
    frames = vs.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vs.get(cv2.CAP_PROP_FPS)

    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f"number of frames: {frames}")
    print(f"duration in seconds: {seconds}")
    print(f"video time: {video_time}")
    print("FPS: " , fps)
    
    writer = None
    (W, H) = (None, None)
    
    set_seconds = 1
#    no_of_frames = int(round(seconds / set_seconds))
    mul = fps * set_seconds
    count = 0
    safe = 0
    notsafe = 0
  
    (grabbed, frame) = vs.read()
    frameId = int(round(vs.get(1)))
    readtime = time.time()
    save = []
    # loop over frames from the video file stream
    while True:
        # read the next frame from the file
        frameId = int(round(vs.get(1))) #current frame number

       # print("FrameID = ", frameId)
        (grabbed, frame) = vs.read() 

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break

        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        output = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame / 255.0
        frame = cv2.resize(frame, (224, 224)).astype("float32")
        save = output

        # frame -= mean

        # make predictions on the frame and then update the predictions
        # queue
        
        if ((frameId != 0) & (frameId % mul == 0)):
            preds = vid_model.predict(np.expand_dims(frame, axis=0))[0]
            print(preds)
            Q.append(preds)
            print("FrameID = ", frameId)
            count = count + 1
            
            # perform prediction averaging over the current history of
            # previous predictions

            results = np.array(Q).mean(axis=0)
        #    print("Average of predictions: ", results)
            i = np.argmax(preds)
            label = labels[i]
            print(label)
        
            #counting safe and not safe labels
            if ((label != "Neutral") & (label != "Drawing")):
                notsafe = notsafe + 1
            else:
                safe = safe + 1
            
            
            # draw the activity on the output frame
            text = "activity: {}:".format(label)
        

            cv2.putText(
                output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 255, 0), 5
            )
        readendtime = time.time()
    #    print("Time to read: ", readendtime - readtime)

        # output_vid = "/output" + file_path.split("/")[-1][:-4] + "--output.mp4"

        output_vid = "D:/Repos-Sadiq/ml-kit-algo/nsfw-classifier-qib/output/videos--output(unsafe2).mp4"
   
    # print(output_vid)
        # check if the video writer is None
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(output_vid, fourcc, 30, (W, H), True)

        # write the output frame to disk
        writer.write(save)

        # show the output image
        # cv2.imshow("Output", output)
        # cv2_imshow(output)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        
     
   # print("Safe content: ", safe)
   # print("Not Safe content: ", notsafe)
    safe_percentage = (safe/count) * 100
    notsafe_percentage = (notsafe / count) * 100
    print("Safe Content Percentage: ", safe_percentage, "%")
    print("Not Safe Content Percentage: ", notsafe_percentage, "%")
    if (safe_percentage > notsafe_percentage):
        print("The content is SAFE")
    else:
        print("The content is NOT SAFE")
        
  #  print("Writing time: ", writingendtime - writetime)
    endTime = time.time()
    elapsedTime = endTime - startTime
    print("Elapsed Time = %s" % elapsedTime)
    print("Frame Count", count)
    # release the file pointers
    print("[INFO] cleaning up...")
    # writer.release()
    vs.release()


if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need filepath to the image
    parser.add_argument("--file_path", type=str)

    # read the arguments from the command line
    args = parser.parse_args()


    # run the predict specified by command line arguments
    startTime = time.time()
    # predict(file_path=args.file_path)
    predict("D:/Repos-Sadiq/ml-kit-algo/nsfw-classifier-qib/data/unsafe1.mp4")


