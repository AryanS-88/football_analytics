from ultralytics import YOLO
import supervision as sv
import pickle
import os
import sys
import cv2
import numpy as np

# Add utility functions directory to path
sys.path.append('../')
from utils import get_centre_of_bbox, get_bbox_width

class tracker:
    def __init__(self, model_path):
        # Load YOLO model
        self.model = YOLO(model_path)
        # Initialize ByteTrack for object tracking
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames):
        # Run YOLO model in batches
        batch_size = 20
        detections = []
        for i in range(0, len(frames), batch_size):
            detections_batch = self.model.predict(frames[i:i+batch_size], conf=0.1)
            detections += detections_batch
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        # Load tracks from file if available
        if read_from_stub and stub_path and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                return pickle.load(f)

        # Detect objects in frames
        detections = self.detect_frames(frames)

        # Initialize tracking dictionary
        tracks = {
            "players": [],
            "referees": [],
            "ball": [],
        }

        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}

            # Convert detections to Supervision format
            detection_supervison = sv.Detections.from_ultralytics(detection)

            # Convert 'goalkeeper' label to 'player'
            for i, cls_id in enumerate(detection_supervison.class_id):
                if cls_names[cls_id] == 'goalkeeper':
                    detection_supervison.class_id[i] = cls_names_inv["player"]

            # Apply ByteTrack tracking
            detection_with_tracks = self.tracker.update_with_detections(detection_supervison)

            # Initialize frame-specific dictionaries
            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})

            # Store player and referee tracks
            for det in detection_with_tracks:
                bbox = det[0].tolist()
                cls_id = det[3]
                track_id = det[4]

                if cls_id == cls_names_inv['player']:
                    tracks["players"][frame_num][track_id] = {"bbox": bbox}
                elif cls_id == cls_names_inv['referee']:
                    tracks["referees"][frame_num][track_id] = {"bbox": bbox}

            # Store ball detections (no tracking)
            for det in detection_supervison:
                bbox = det[0].tolist()
                cls_id = det[3]
                if cls_id == cls_names_inv['ball']:
                    tracks["ball"][frame_num][1] = {"bbox": bbox}

        # Save tracking data to stub path
        if stub_path:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)

        return tracks

    def draw_ellipse(self,frame,bbox,color,track_id=None):
        y2 = int(bbox[3])
        x_center, _ =get_centre_of_bbox(bbox)
        width = get_bbox_width(bbox)

        cv2.ellipse(
            frame,
            center=(x_center,y2),
            axes=(int(width), int(0.35*width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color = color,
            thickness=2,
            lineType=cv2.LINE_4
        )

        rectangle_width = 40
        rectangle_height=20
        x1_rect = x_center - rectangle_width//2
        x2_rect = x_center + rectangle_width//2
        y1_rect = (y2- rectangle_height//2) +15
        y2_rect = (y2+ rectangle_height//2) +15

        if track_id is not None:
            cv2.rectangle(frame,
                          (int(x1_rect),int(y1_rect) ),
                          (int(x2_rect),int(y2_rect)),
                          color,
                          cv2.FILLED)
            
            x1_text = x1_rect+12
            if track_id > 99:
                x1_text -=10
            
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text),int(y1_rect+15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,0),
                2
            )

        return frame
    def draw_traingle(self,frame,bbox,color):
        y= int(bbox[1])
        x,_ = get_centre_of_bbox(bbox)

        triangle_points = np.array([
            [x,y],
            [x-10,y-20],
            [x+10,y-20],
        ])
        cv2.drawContours(frame, [triangle_points],0,color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points],0,(0,0,0), 2)

        return frame

    def draw_annotation(self, video_frames, tracks):
        # Overlay tracked player annotations on video frames
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks["players"][frame_num]
            ball_dict = tracks["ball"][frame_num]
            referee_dict = tracks["referees"][frame_num]

            # Draw players
            for track_id, player in player_dict.items():
                frame = self.draw_ellipse(frame, player["bbox"], (0, 0, 255), track_id)

            # Draw Referees
            for _, referee in referee_dict.items():
                frame = self.draw_ellipse(frame, referee["bbox"], (0, 255, 255), track_id)
            
            # Draw Ball
            for track_id,ball in ball_dict.items():
                frame = self.draw_traingle(frame, ball["bbox"], (255, 0, 0))

            output_video_frames.append(frame)

        return output_video_frames
