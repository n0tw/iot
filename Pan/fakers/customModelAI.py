import cv2

from ultralytics import YOLO
import supervision as sv
import numpy as np
import warnings
import torch
warnings.simplefilter(action='ignore', category=FutureWarning)

ZONE_POLYGON = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

def process_video():
    frame_width = 852
    frame_height = 480

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("C:/Users/pangl/Desktop/IoT_project/prytan.mp4")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model1 = YOLO("yolov8l.pt")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/pangl/Desktop/IoT_project/crowdhuman_yolov5m.pt')

    box_annotator = sv.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale=0.5,
        text_padding=1
    )

    zone_polygon = (ZONE_POLYGON * np.array([round((4/5)*frame_width), frame_height])).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple([frame_width, frame_height]))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.red(),
        thickness=1,
        text_thickness=2,
        text_scale=1
    )

    frame_counter = 0
    bus_detection = False

    while True:
        ret, frame = cap.read()

        if(frame_counter % 300 == 0):  # Process every 300 frames
            # People counter
            result = model(frame)
            detections = sv.Detections.from_yolov5(result)
            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, _
                in detections
            ]
            detections_0 = detections[detections.class_id == 0]
            frame = box_annotator.annotate(
                scene=frame, 
                detections=detections_0,
                labels=labels
            )

            # # Bus detection
            # result1 = model1(frame, agnostic_nms = True, classes=[5])[0]
            # detections1 = sv.Detections.from_yolov8(result1)    
            # labels1 = [
            #     f"{model1.model.names[class_id1]} {confidence1:0.2f}"
            #     for _, confidence1, class_id1, _
            #     in detections1
            # ]
            # frame = box_annotator.annotate(
            #     scene=frame, 
            #     detections=detections1,
            #     labels=labels1
            # )
            # if(len(detections1)!=0): bus_detection = True
            # else: bus_detection = False

            yield len(detections_0)
            
            
            zone.trigger(detections = detections_0)
            frame = zone_annotator.annotate(scene=frame)      
        
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(1) == ord('q')):
            break

        frame_counter += 1

if __name__ == "__main__":
    video_processor = process_video()
    
    while True:
        try:
            counter_values = next(video_processor)
            print(f"People counter value: {counter_values}")
        except StopIteration:
            break
