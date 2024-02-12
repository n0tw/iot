1. Download all files and put them in a folder
2. In the folder path, open cmd and type ~pip install Flask pymongo Flask-RESTful requests aiohttp flask schedule opencv-python torch ultralytics supervisely paho-mqtt numpy pandas torchvision detectron2
3. In the cmd, type ~pip show numpy. Open the package location and go to supervision>detection>core.py and change np.bool to bool in line 175. Then save.
4. Download docker for windows.
5. In externalDB folder open cmd and type docker compose -up --build
6. Run the python files in order: notifyDriver.py > edgeControllerSyncSupport.py > edgeController.py > busStopFaker.py > send_buses_onthe_road.py

