1. Download all files and put them in a folder
2. In the folder path, open cmd and type ~pip install Flask pymongo Flask-RESTful requests aiohttp flask schedule opencv-python torch ultralytics supervisely paho-mqtt numpy pandas torchvision detectron2
3. In the cmd, type ~pip show numpy. Open the package location and go to supervision>detection>core.py and change np.bool to bool in line 175. Then save.
4. Download GitRepo_LargeFiles
5. In busStopFaker.py, in line 274 change the file path to path of prytan.mp4 located in GitRepo_LargeFiles. In line 282, change the path of crowdhuman_yolov5m.pt too.
6. In busai.py, in lines 263 and 168 do the same for Routes.xlsx. In line 35 do it for iot_bus.mp4 and in line 37 do it for yolo8s.pt.
7. In send_buses_onthe_road.py, in line 14 add the path of busai.py.
8. Download docker for windows.
9. In externalDB folder open cmd and type docker compose -up --build
10. Run the python files in order: notifyDriver.py > edgeControllerSyncSupport.py > edgeController.py > busStopFaker.py > send_buses_onthe_road.py

