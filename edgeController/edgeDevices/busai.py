import datetime
import os
import asyncio
import threading
import random
import cv2
import requests
import numpy as np
import pandas as pd
from flask import Flask, request
import aiohttp
from ultralytics import YOLO
import detectron2
import supervision as sv
import torch
import ultralytics
import sys

TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch:", TORCH_VERSION, "; cuda:", CUDA_VERSION)

HOME = os.getcwd()
print(HOME)

# Install YOLOv5
from IPython import display
display.clear_output()

ultralytics.checks()
print("detectron2:", detectron2.__version__)
print("supervision", sv.__version__)

# Download data
# Current folder
current_script_directory = os.path.dirname(os.path.realpath(__file__))

# Navigate to the parent folder
parent_folder = os.path.abspath(os.path.join(current_script_directory, os.pardir))
parent_of_parent = os.path.abspath(os.path.join(parent_folder, os.pardir))

# Specify the file name you want to access in the parent folder
file_in_parent_folder = os.path.join(parent_of_parent, 'GitRepo_LargeFiles/bus-raspberry')

SUBWAY_VIDEO_PATH = os.path.join(file_in_parent_folder, "iot_bus.mp4")
YOLO_PATH = os.path.join(file_in_parent_folder, "yolov8s.pt")

model = YOLO(YOLO_PATH)

async def async_http_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

ids = sys.argv[1:]

# Check if ids are provided
if ids:
    print("Received ids:", ids)
else:
    print("No ids provided.")

crowdflowid = ids[0]
vehicleid = ids[1]

Favierou_vid = 0
video_ended_event = threading.Event()

app = Flask(__name__)

@app.route('/video_ended', methods=['POST'])
def handle_request():
    global Favierou_vid
    data = request.get_json()
    favierou_vid_param = data['favierou_vid']

    if favierou_vid_param is not None:
        Favierou_vid = int(favierou_vid_param)
        print("\n")
        print("\n")
        print(Favierou_vid)
        print("\n")
        print("\n")
        if Favierou_vid == 1:
            video_ended_event.set()
        return 'Request handled successfully'
    else:
        return 'Missing "favierou_vid" parameter', 400

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

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
max_people = 0
processing_video = False

async def send_data_async(locations):
    edge_controller_url = 'http://localhost:5002/receive_bus_data'
    data = {"locations": locations[0]['Location'], "vehicleid": vehicleid, "crowdflowid": crowdflowid, "busnumber": "601"}

    try:
        await async_http_request(edge_controller_url, data)
        print("Data sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

async def send_to_station_async(max_people, station_info):
    station_url = 'http://localhost:5001/receive_data'
    data = {"vehicleid": vehicleid, "station_name": station_info[0][0]['Station'],
            "station_location": station_info[1][0]["Station's Location"]}
    print(data)
    try:
        await async_http_request(station_url, data)
        print("Data sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

    edge_controller_crowd_url = 'http://localhost:5002/receive_crowd_data'
    crowdFlowSplitted = crowdflowid.split(':')
    idNumber = crowdFlowSplitted[-1]
    crowd_data = {'id': crowdflowid, 'value': max_people, 'dateObserved': datetime.datetime.now().isoformat(),
                  'station': station_info[0][0]['Station'], 'entityName': f"Bus {idNumber}"}

    try:
        await async_http_request(edge_controller_crowd_url, crowd_data)
        print("Data sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

async def read_locations(file_path, start_row=None, end_row=None, skip_value=None):
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
                df2 = pd.read_excel(file_path, usecols=[3], skiprows=skiprows, nrows=nrows)
                st_loc = df2.to_dict(orient='records')
                return locations, [stations, st_loc]
            else:
                return locations, False
        else:
            if start_row + 1 < 123:
                return await read_locations(
                    file_path=os.path.join(file_in_parent_folder, "Routes.xlsx"),
                    start_row=start_row + 1,
                    end_row=end_row + 1,
                    skip_value="-"
                )
            else:
                return locations, False
    except Exception as e:
        print(f"Error reading locations from Excel: {e}")
        return [], False

async def process_frame_async(frame: np.ndarray, _) -> np.ndarray:
    global max_people
    results = model(frame, imgsz=1280)[0]
    detections = sv.Detections.from_yolov8(results)
    detections = detections[detections.class_id == 0]
    zone.trigger(detections=detections)

    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
    labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
    frame = zone_annotator.annotate(scene=frame)
    z = zone.trigger(detections=detections)

    if sum(z) > max_people:
        max_people = sum(z)

    additional_info_text = f"People inside: {max_people}"

    cv2.putText(frame, additional_info_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 6, cv2.LINE_AA)

    return frame, max_people

async def faker_async(station, location):
    global max_people
    random_integer = random.randint(-30, 30)

    if max_people + random_integer >= 0:
        max_people += random_integer
    else:
        max_people = 0

    await send_data_async(location)
    await send_to_station_async(int(max_people), station)
    print(max_people)

async def start_video_async(station, location):
    cap = cv2.VideoCapture(SUBWAY_VIDEO_PATH)
    global processing_video, max_people
    frame_counter = 0

    await send_to_station_async(int(max_people), station)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while processing_video:
        ret, frame = cap.read()

        if not ret:
            print("Video has ended.")
            break

        frame_counter += 1

        if frame_counter % 20 == 0:
            processed_frame, max_val = await process_frame_async(frame, None)
            cv2.imshow("Video", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if frame_counter == 20:
            frame_counter = 0

    if max_people + max_val >= 0:
        max_people += max_val
    else:
        max_people = 0

    await send_to_station_async(int(max_people), station)
    await send_data_async(location)

    print(max_people)

    cap.release()
    cv2.destroyAllWindows()

async def update_locations_async():
    global row, processing_video, video_ended_event
    row = 1

    while True:
        excel_file_path = os.path.join(file_in_parent_folder, "Routes.xlsx")
        result = await read_locations(
            file_path=excel_file_path,
            start_row=row,
            end_row=row,
            skip_value="-"
        )

        if result is not None:
            locations, station = result
            await send_data_async(locations)
            print(locations)
            t = 1
            if station:
                t = 3
                print("station[0]", station[0])
                if station[0] == [{'Station': 'Ermou'}]:
                    print(station)
                    processing_video = True

                    # Start video processing thread
                    video_thread = threading.Thread(target=await_start_video_async, args=(station, locations))
                    video_thread.start()
                    video_thread.join()

                    processing_video = False
                elif station[0] == [{'Station': 'Favierou'}]:
                    await faker_async(station, locations)
                    video_ended_event.wait()
                    video_ended_event.clear()
                elif station[0] == [{'Station': 'Hospital'}]:
                    await faker_async(station, locations)
                    row = 0
                else:
                    await faker_async(station, locations)

            row += 1
        else:
            print("Error reading locations. Stopping update.")
            break
        await asyncio.sleep(t)

# Function to run start_video_async in the event loop
def await_start_video_async(station, locations):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_video_async(station, locations))

async def main():
    # Start the Flask app
    from threading import Thread
    Thread(target=app.run, kwargs={'port': 5000}).start()

    # Start the location update task
    locations_task = asyncio.create_task(update_locations_async())

    # Wait for both tasks to complete
    await asyncio.gather(locations_task)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
