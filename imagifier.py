import os
import numpy

import cv2
class Imagifier : 
  def __init__(self , filename , token , folder ):
    for filename in os.listdir(directory):
      vidcap = cv2.VideoCapture(directory+'/'+filename)
      count = 0
      while True:
          success,image = vidcap.read()
          if not success:
              break
          if count%5 == 0 :
            cv2.imwrite(os.path.join(folder,"frame{:d}.jpg".format(count)), image) 
            file1 = open("/content/drive/My Drive/saved/static/data_list/Deepfakes_c0_test.txt","a") 
            file1.write(f"{folder}/frame{count}.jpg "+ token +"\n") 
            file1.close()
          count += 1
    print("{} images are extacted in {}.".format(count,folder))