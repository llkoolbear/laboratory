# ===============================================================================
#
# Name:       robot_watch_youtube.py 
#
# Purpose:    Program for robot to watch youtube videos and rate them
#
# Author:     Bear Bissen
#
# Created:    April 24, 2022
# Last Rev:   
# Edited by:  
#
# License: MIT Open License
#
# ===============================================================================

from facetracker_bb import FaceTracker
from youtube_watcher.youtube_watcher import YoutubeWatcher

if __name__ == '__main__':
    try:
        youtube_watcher = YoutubeWatcher()
        face_tracker = FaceTracker()
        face_tracker.track_face()
        youtube_watcher.youtube_search('robot')
        youtube_watcher.watch_videos()
    except KeyboardInterrupt:
        print("User Pressed Keyboard ctrl-c")
    finally:
        face_tracker.stop_track()
        youtube_watcher.stop_video()
        print("Stopped Tracking")