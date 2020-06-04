from flask import Flask , render_template 
from flask_ngrok import run_with_ngrok
from flask import session, url_for 
from flask import * 
from tqdm import tqdm
from flask import request
import dlib
import time 
import os 
import shutil
from static.detect_from_video import detect 
from static.imagifier import Imagifier 
from static.train_CNN import Train 
from flask_dropzone import Dropzone
app = Flask(__name__)
app.secret_key = "abd"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
run_with_ngrok(app)  
app.config.update(
  DROPZONE_MAX_FILE_SIZE=3000000,
  DROPZONE_MAX_FILES=300,
  DROPZONE_PARALLEL_UPLOADS=200,  # set parallel amount
  DROPZONE_TIMEOUT = 9999999 , 
  DROPZONE_UPLOAD_MULTIPLE=True  # enable upload multiple
)

dropzone = Dropzone(app)
@app.route("/")
def root():
  session["pbar"] = 0 
  session["fakeOrReal"] = 0 

  return render_template("home.html")
@app.route("/home")
def home():
  return render_template("upload.html")
@app.route("/train")
def train():
  return render_template("train.html")

@app.route('/a', methods=['POST', 'GET'])
def uploada():
  if request.method == 'POST':
     for key, f in request.files.items():
        if key.startswith('file'):
          f.save(os.path.join("/content/sample_data", f.filename))
  return "OK"


@app.route('/b', methods=['POST', 'GET'])
def uploadb():
  if not os.path.isdir("/content/DeepFakeDetectionGUI/images/videosForTest"):
    os.mkdir("/content/DeepFakeDetectionGUI/images/videosForTest")
  if request.method == 'POST':
     for key, f in request.files.items():
        if key.startswith('file'):
          f.save(os.path.join("/content/DeepFakeDetectionGUI/images/videosForTest", f.filename))
  return "OK"

@app.route("/route-module")
def module():
  folderR = '/content/real'  
  folderF = '/content/real/fake'  
  targetMR = os.path.join(APP_ROOT , 'static/moduleVideos/real')
  targetMF = os.path.join(APP_ROOT , 'static/moduleVideos/fake')
  print ('called')
  try:
    if os.path.isdir(folderR):     
      shutil.rmtree(folderR)
    if os.path.isdir(folderF):     
      shutil.rmtree(folderF)
    shutil.rmtree(targetMR)
    shutil.rmtree(targetMF)
    shutil.rmtree("/content/DeepFakeDetectionGUI/static/result")
    
  except:
   print('Error while deleting directory')

  os.mkdir(targetMR)
  os.mkdir(targetMF)

  id1 = 0
  id2 = 0 
  
  for file in os.listdir("/content/sample_data"):  
    if "FAKE" in  file :
      destinat  = "/".join([targetMF , str(id1)])
      print(destinat)
      shutil.move("/content/sample_data/"+file, destinat)
      id1 = id1 +1
    if "REAL" in  file:
      destinat  = "/".join([targetMR  , str(id2)])
      print(destinat)
      shutil.move("/content/sample_data/"+file, destinat)
      id2 = id2 +1
      
  os.mkdir(folderR)
  os.mkdir(folderF)
  open("/content/DeepFakeDetectionGUI/static/data_list/Deepfakes_c0_test.txt", 'w').close()
  iR = Imagifier("/content/DeepFakeDetectionGUI/static/moduleVideos/real" , "1", folderR)
  iF = Imagifier("/content/DeepFakeDetectionGUI/static/moduleVideos/fake" , "0", folderF)

  T = Train()
  return jsonify("1")


@app.route("/route")
def upload():
  if os.path.isfile("/content/DeepFakeDetectionGUI/static/videos/output/003_000.mp4"):
    os.remove("/content/DeepFakeDetectionGUI/static/videos/output/003_000.mp4")
  if os.path.isfile("/content/DeepFakeDetectionGUI/static/videos/output/003_000.avi"):  
    os.remove("/content/DeepFakeDetectionGUI/static/videos/output/003_000.avi")
  if os.path.isfile("/content/DeepFakeDetectionGUI/static/videos/003_000.mp4"):  
    os.remove("/content/DeepFakeDetectionGUI/static/videos/003_000.mp4")
  target = os.path.join(APP_ROOT , 'static/videos')
  print (target)
  destination  = "/".join([target , "003_000.mp4"])
  print(destination)
  if not os.path.isdir(target):
    os.mkdir(target)
  trigger = 0
  for file in os.listdir("/content/DeepFakeDetectionGUI/images/videosForTest"):  
    print(file)
    if "MODEL" in  file :
      trigger = 1 
      destinat  = "/".join(["/content/DeepFakeDetectionGUI/static/pretrained_model" , str("0")])
      shutil.move("/content/DeepFakeDetectionGUI/images/videosForTest/"+file, destinat)
    else : 
      shutil.move("/content/DeepFakeDetectionGUI/images/videosForTest/"+file, destination)

  if trigger : 
    d = detect("/content/DeepFakeDetectionGUI/static/videos/003_000.mp4" , "/content/DeepFakeDetectionGUI/static/pretrained_model/best0.pkl" , "/content/DeepFakeDetectionGUI/static/videos/output")
  else: 
    d = detect("/content/DeepFakeDetectionGUI/static/videos/003_000.mp4" , "/content/DeepFakeDetectionGUI/static/pretrained_model/df_c0_best.pkl" , "/content/DeepFakeDetectionGUI/static/videos/output")
  print(d.pbar)
  print(d.labels)
  if os.path.isdir("/content/DeepFakeDetectionGUI/images/videosForTest"):     
      shutil.rmtree("/content/DeepFakeDetectionGUI/images/videosForTest") 
  os.mkdir("/content/DeepFakeDetectionGUI/images/videosForTest")
  
  session["result"] = 0
  session["pbar"] = str(d.pbar)
  if d.labels[0] > d.labels[1] * 3 :
    session["result"] = "REAL"
    session["fakeOrReal"] = "success" 
  else : 
    session["result"] = "FAKE"
    session["fakeOrReal"] = "danger" 
  
  def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
    return True
  convert_avi_to_mp4("/content/DeepFakeDetectionGUI/static/videos/output/003_000.avi", "/content/DeepFakeDetectionGUI/static/videos/output/003_000")  
  time.sleep(20)
  return jsonify("1")

@app.route('/upload-complete' )      
def upload_complete():
  while not os.path.exists("/content/DeepFakeDetectionGUI/static/videos/output/003_000.mp4"):
    time.sleep(1)
  if os.path.isfile("/content/DeepFakeDetectionGUI/static/videos/output/003_000.mp4"):
    return render_template("complete.html" , val1 = session['pbar'] , val2= session["fakeOrReal"] , val3 = session["result"] ) ; 


@app.route('/module-complete')      
def module_complete():  
  arr = []
  for filename in os.listdir("/content/DeepFakeDetectionGUI/static/result"):  
    if 'model' in filename:
      arr.append(filename)
  return render_template("train_complete.html" , filenames = arr  )


app.run()
