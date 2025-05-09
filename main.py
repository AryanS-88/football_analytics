from utils import read_video, save_video
from trackers import tracker
import cv2
import os
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner

def main():
    # Read video 
    video_frames = read_video("input_videos/08fd33_4.mp4")

    # Initialize tracker
    Tracker = tracker("models/best.pt")
    tracks = Tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path="stubs/track_stubs.pkl")
    
    #Interpolate Ball Positions 
    tracks["ball"]=Tracker.interpolate_ball_position(tracks["ball"])
    
    #assign player teams 
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], 
                                    tracks['players'][1])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num],   
                                                 track['bbox'],
                                                 player_id)
            tracks['players'][frame_num][player_id]['team'] = team 
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]


    # assign ball Aquisition
    player_ball_assigner = PlayerBallAssigner()
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_ball_assigner.assign_ball_to_player(player_track,ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True

    # Draw object tracks
    output_video_frames = Tracker.draw_annotation(video_frames, tracks)

    # Save video
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()
