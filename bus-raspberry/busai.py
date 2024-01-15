import torch
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)

import os
HOME = os.getcwd()
print(HOME)

"""## Install YOLOv5"""

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

import subprocess

import detectron2
print("detectron2:", detectron2.__version__)


import supervision as sv
print("supervision", sv.__version__)

"""## Download data"""

SUBWAY_VIDEO_PATH = "C:/Users/eugk/Documents/iot/project/iot_bus.mp4"

from ultralytics import YOLO
model = YOLO('yolov8s.pt')

import numpy as np
import supervision as sv
import cv2
import requests
import pandas as pd
import threading
import time
import random
import queue

video_info = sv.VideoInfo.from_video_path(SUBWAY_VIDEO_PATH)
print("video_info", video_info)
# initiate polygon zone
polygon = np.array([
    [0, 1920],
    [0, 1920//2],
    [1080, 1920//2],
    [1080, 1920]
])
zone = sv.PolygonZone(polygon=polygon, frame_resolution_wh=video_info.resolution_wh)

# initiate annotators
box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.white(), thickness=6, text_thickness=6, text_scale=4)
max=0

z_1 = [False]
m=0
max_people = 0
processing_video = False 

def send_data(max_value, locations):
    edge_controller_url = "http://edge-controller-url" 
    data = {"max_value": max_value, "locations": locations}
    
    try:
        response = requests.post(edge_controller_url, json=data)
        response.raise_for_status()
        print("Data sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def send_to_station(max_value, locations):
    station_url = "http://station-url" 
    data = {"max_value": max_value, "locations": locations}
    
    try:
        response = requests.post(station_url, json=data)
        response.raise_for_status()
        print("Data sent successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def read_locations(file_path, start_row=None, end_row=None, skip_value=None):
    try:
        use_cols = [1]
        skiprows = range(1, start_row) if start_row else None
        nrows = end_row - start_row + 1 if start_row and end_row else None

        df = pd.read_excel(file_path, usecols=use_cols, skiprows=skiprows, nrows=nrows)
        df1 = pd.read_excel(file_path, usecols=[2], skiprows=skiprows, nrows=nrows)
        
        if skip_value is not None:
            df = df[~df.iloc[:, 0].apply(lambda x: str(x) == str(skip_value))]
            df1 = df1[~df1.iloc[:, 0].apply(lambda x: str(x) == str(skip_value))]
        
        locations = df.to_dict(orient='records')
        stations = df1.to_dict(orient='records')

        if not df.empty:
            if not df1.empty:
                return locations, stations
            else:
                return locations, False
        else:
            if start_row + 1<123:
                print("No valid locations found in row {}. Trying next row.".format(start_row))
                return read_locations(
                    file_path="Routes.xlsx",
                    start_row=start_row + 1,
                    end_row=end_row+1,
                    skip_value="-"
                )
            else:
                return locations, False
    except Exception as e:
        print(f"Error reading locations from Excel: {e}")
        return [], False

def process_frame(frame: np.ndarray, _) -> np.ndarray:
    global z_1, max, m
    results = model(frame, imgsz=1280)[0]
    detections = sv.Detections.from_yolov8(results)
    detections = detections[detections.class_id == 0]
    zone.trigger(detections=detections)

    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
    labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
    frame = zone_annotator.annotate(scene=frame)
    z = zone.trigger(detections=detections)
    if m==0:
       max=sum(z)
       m=1
    if sum(z)>max:
        max= sum(z)
    if len(z_1) == len(z):
        for i,k in enumerate(z_1):
            if z[i]==False and z_1[i]==True:
                max=max-1
            #if z[i]==True and z_1[i]==False:
            #    max=max+1
 
    print("δετεψτιονσ", max )
    z_1= z

    additional_info_text = f"People inside: {max}"
    
    cv2.putText(frame, additional_info_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 6, cv2.LINE_AA)
    
    #sv.show_frame_in_notebook(frame, (16, 16))
    return frame, max

cap = cv2.VideoCapture(SUBWAY_VIDEO_PATH)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

def faker(station):
    random_integer = random.randint(1, 30)
    print(station)
    print(random_integer)


def start_video():
    cap = cv2.VideoCapture(SUBWAY_VIDEO_PATH)
    global processing_video, max_people

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while processing_video:
        ret, frame = cap.read()

        if not ret:
            print("Video has ended.")
            break

        processed_frame, max_people = process_frame(frame, None)

        cv2.imshow("Video", processed_frame)

        # Check if the user pressed 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(max_people)
    cap.release()
    cv2.destroyAllWindows()


def update_locations():
    global row, processing_video
    row = 1
    end_row = 123

    while row <= end_row:
        excel_file_path = "Routes.xlsx"
        result = read_locations(
            file_path=excel_file_path,
            start_row=row,
            end_row=row,
            skip_value="-"
        )
        
        if result is not None:
            locations, station = result
            print(locations)
            
            if station:
                if station == [{'Stations': 'Ermou'}]:
                    print(station)
                    processing_video = True

                    # Start video processing thread
                    video_thread = threading.Thread(target=start_video)
                    video_thread.start()

                    # Wait for the video processing thread to finish
                    video_thread.join()

                    processing_video = False
                else:
                    faker(station)
            
            row += 1
        else:
            print("Error reading locations. Stopping update.")
            break
        time.sleep(3)

# Start the location update thread
locations_thread = threading.Thread(target=update_locations)
locations_thread.start()

locations_thread.join() 

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()