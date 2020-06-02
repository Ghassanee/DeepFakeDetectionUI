# DeepFakeDetectionGUI
---
## Use google colab
1. Go to https://colab.research.google.com
2. make a **new notebook**
3. make sure that you are using a the right runtime : **Runtime => change runtime type => GPU** 
4. Enjoy!
---
## clone 
```
!git clone https://github.com/ghassane20a/DeepFakeDetectionGUI.git
```
---------
## install requirements
```
!pip install flask-ngrok
!pip install flask
!pip install flask-dropzone
```
---
## cd to project file 
```
cd DeepFakeDetectionGUI/
```
---
## start the app 
```
!python main.py


```
click in the **ngrok** link like : "http://bc8621095968.ngrok.io"

## Problem you may see

if you got this problem 
```
tunnel url = j['tunnels'][0]['public_url'] # Do the parsing of the get
indexerror: list index out of range
```
**you should make another notebook or restart your runtime**
