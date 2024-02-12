# Required apps:

+ Download and install Nodejs from the official Node.js website: https://nodejs.org/
+ Download docker desktop from https://docs.docker.com/desktop/install/windows-install/ 

# Required packages:

## Python packages:
+ For python packages needed run:
```cmd
pip install Flask pymongo Flask-RESTful requests aiohttp flask schedule opencv-python torch ultralytics supervisely paho-mqtt numpy pandas torchvision detectron2
```

## Node.js packages:
+ For Express run: npm install express
+ For Cors run: npm install cors
+ For For Axios run: npm install axios
+ For Body-parser run: npm install body-parser
+ For Node-fetch run: npm install node-fetch@2.6.1
+ For Nodemailer run: npm install nodemailer
+ For XLSX run: npm install xlsx
+ For socket.io run: npm install socket.io

# How to run:

1. Download all files and put them in a folder
   + Download GitRepo_LargeFiles from [here](https://www.dropbox.com/scl/fo/xkffl87ia2yy5pp4ahwvg/h?rlkey=nb8zr8kwkz41wdny6tdgwtgec&dl=0) and add it in the same folder as the rest of the files
        
2. In the cmd, type ~pip show numpy. Open the package location and go to supervision>detection>core.py and change np.bool to bool in line 175. Then save.
   
3. In externalDB folder open cmd and type ~docker compose -up --build
    
4. In edgeController folder open cmd and type ~python run_scripts.py

5. In frontEnd-backEnd folder open cmd and tpye ~node start-scripts.js
