import os
import numpy

import cv2
class Imagifier : 
  count = 0
  def __init__(self , directory , token , folder ):
    for filename in os.listdir(directory):
      vidcap = cv2.VideoCapture(directory+'/'+filename)
      while True:
          success,image = vidcap.read()
          if not success:
              break
          if self.count%5 == 0 :
            cv2.imwrite(os.path.join(folder,"frame{:d}.jpg".format(self.count)), image) 
            file1 = open("/content/gdrive/My Drive/saved/static/data_list/Deepfakes_c0_test.txt","a") 
            file1.write(f"{folder}/frame{self.count}.jpg "+ token +"\n") 
            file1.close()
          self.count += 1
    print("{} images are extacted in {}.".format(self.count,folder))