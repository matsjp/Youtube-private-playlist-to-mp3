from videos.Video import Video


class Playlist:
    def __init__(self, api, playlist_id):
        self.api = api
        self.video_list = []
        self.playlist_id = playlist_id

    def get_videos(self):
        self.video_list = []
        temp = self.api.get('playlistItems', playlistId=self.playlist_id, maxResults='50').json()
        items = temp['items']
        for item in items:
            self.video_list.append(Video(item['snippet']['resourceId']['videoId'], item['id']))

    def delete_video(self, video):
        if video in self.video_list:
            self.api.delete('playlistItems', id=video.playlist_item_id)
            self.video_list.remove(video)
        else:
            print('Video to be deleted doesn\'t exist')

    def add_video(self, video):
        body = {
            'snippet': {
                'playlistId': self.playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video.video_id
                }
            }
        }
        self.api.post('playlistItems', body=body)