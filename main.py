from utils import read_video, save_video
from trackers import tracker

def main():
    # Read video 
    video_frames = read_video("input_videos/08fd33_4.mp4")

    # Initialize tracker
    Tracker = tracker("models/best.pt")
    tracks = Tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path="stubs/track_stubs.pkl")

    # Draw object tracks
    output_video_frames = Tracker.draw_annotation(video_frames, tracks)

    # Save video
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()
