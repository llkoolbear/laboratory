# ===============================================================================
#
# Name:       youtube_watcher.py 
#
# Purpose:    Watches a youtube video and rates it when it's finished
#
# Author:     Bear Bissen
#
# Created:    August 13, 2022
# Last Rev:   August 13, 2022
# Edited by:  Bear Bissen
#
# License: MIT Open License
#
# ===============================================================================

from googleapiclient.sample_tools import init
from selenium import webdriver
import time
import isodate
import os

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
CLIENT_SECRETS_FILE = os.path.join(CURRENT_DIR, 'client_secret.json')
CREDENTIALS_FILE = os.path.join(CURRENT_DIR, 'youtube.dat')

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
ARGS = [] # placeholder for args

RATINGS = ('like', 'dislike', 'none')

class YoutubeWatcher:

    def __init__(self):
        self.video = self.Video
        self.videos = []
        self.channels = []
        self.playlists = []
        self.browser = None
        self.youtube = init(ARGS, API_SERVICE_NAME, API_VERSION, API_SERVICE_NAME, CLIENT_SECRETS_FILE)[0]
        self.search_results = None

    def youtube_search(self, search_term, max_results=10):

        # Call the search.list method to retrieve results matching the specified
        # query term.
        self.search_results = self.youtube.search().list(
            q=search_term,
            part='id,snippet',
            maxResults=max_results
        ).execute().get('items', [])

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in self.search_results:
            print(search_result['snippet'], search_result['id'])
            if search_result['id']['kind'] == 'youtube#video':
                self.videos.append('%s (%s)' % (search_result['snippet']['title'],
                                            search_result['id']['videoId']))
            elif search_result['id']['kind'] == 'youtube#channel':
                self.channels.append('%s (%s)' % (search_result['snippet']['title'],
                                            search_result['id']['channelId']))
            elif search_result['id']['kind'] == 'youtube#playlist':
                self.playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                            search_result['id']['playlistId']))

        print('Videos:\n', '\n'.join(self.videos), '\n')
        print('Channels:\n', '\n'.join(self.channels), '\n')
        print('Playlists:\n', '\n'.join(self.playlists), '\n')

    # Add the video rating. This code sets the rating to 'like,' but you could
    # also support an additional option that supports values of 'like' and
    # 'dislike.'
    def like_video(self):
        self.youtube.videos().rate(
            id=self.video.videoId,
            rating=self.video.rating
        ).execute()

    class Video:
        def __init__(self, videoId = None, metadata = None):
            self.videoId = videoId
            self.metadata = metadata
            self.description = None
            self.duration = None
            self.rating = 'none'

            if self.metadata is not None:
                self.description = self.metadata['snippet']['description']
                self.duration = isodate.parse_duration(self.metadata['contentDetails']['duration']).seconds

    def select_video_from_search(self, search_result):
        videoId = search_result['id']['videoId']
        self.video = self.Video(videoId,self.youtube.get_video_metadata(videoId, part = 'snippet,contentDetails'))

    def open_video(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.youtube.com/watch?v=' + self.video.videoId)

    def watch_videos(self):
        for search_result in self.search_results:
            self.select_video_from_search(search_result)
            self.open_video()
            self.watch_video()
            time.sleep(1)

    def stop_video(self):
        self.browser.quit()
        print('Video stopped')

    def watch_video(self):
        start_watch = time.time()
        time_elapsed = 0
        
        while time_elapsed < self.video.duration:
            time_elapsed = time.time() - start_watch
            print('Time elapsed: ' + str(time_elapsed))
            time.sleep(1)

        self.like_video()
        self.browser.quit()
        print('Video watched')
            
if __name__ == '__main__':
    try:
        youtube_watcher = YoutubeWatcher()
        youtube_watcher.youtube_search('robot')
        youtube_watcher.watch_videos()
    except KeyboardInterrupt:
        print("User Pressed Keyboard ctrl-c")
    finally:
        youtube_watcher.stop_video()
        print("Stopped Watching Youtube")