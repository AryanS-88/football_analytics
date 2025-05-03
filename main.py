from utils import read_video, save_video
from trackers import tracker
import cv2
import os

def main():
    # Read video 
    video_frames = read_video("input_videos/08fd33_4.mp4")

    # Initialize tracker
    Tracker = tracker("models/best.pt")
    tracks = Tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path="stubs/track_stubs.pkl")


    # # Save cropped images of players in the first frame
    # for track_id, player in tracks['players'][0].items():
    #     bbox = player["bbox"]  # Extract the actual bbox list
    #     frame = video_frames[0]

    #     # Convert to int to avoid slicing errors
    #     x1, y1, x2, y2 = map(int, bbox)
    #     cropped_image = frame[y1:y2, x1:x2]

    #     # Save image
    #     cv2.imwrite(f"output_videos/cropped_image.jpg", cropped_image)

    # Draw object tracks
    output_video_frames = Tracker.draw_annotation(video_frames, tracks)

    # Save video
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()
