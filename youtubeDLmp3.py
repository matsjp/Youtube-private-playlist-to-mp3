from videos.Playlist import Playlist
from api.YoutubeAPI import YoutubeAPI
from pytube import YouTube
import os
import configparser
from ftplib import FTP


def get_config():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config
    except IOError:
        print('Could not open config.ini')
        exit()


def download():
    print('Starting download')
    api = YoutubeAPI()
    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
    api.authorize('client_secret.json', scopes)
    download_playlist = Playlist(api, 'PLjgXl-YMEXoEoH5jJCZXCF7XzW7y-wrvE')
    backup_playlist = Playlist(api, 'PLjgXl-YMEXoGMnm6AzsX60XM75guUFrJD')

    download_playlist.get_videos()
    for video in download_playlist.video_list:
        print(video.video_id)
        yt = YouTube('http://youtube.com/watch?v=' + video.video_id)
        print('Downloading video: ' + yt.title)
        yt.streams.filter(only_audio=True).first().download('downloads')
        backup_playlist.add_video(video)
        download_playlist.delete_video(video)


def convert():
    print('Starting conversion')
    conversion_list = [f for f in os.listdir('downloads') if os.path.isfile(os.path.join('downloads', f))]
    for file in conversion_list:
        print('Converting: ' + file)
        os.system('ffmpeg.exe -i "downloads/' + file + '" "mp3/' + file[:-4] + '.mp3"')


def ftp(host, port, username, password):
    print('Starting ftp')
    ftp = FTP()
    ftp.encoding='utf-8'
    ftp.connect(host, port)
    print('Connected')
    ftp.login(username, password)
    print('Logged in')
    mp3_files = [f for f in os.listdir('mp3') if os.path.isfile(os.path.join('mp3', f))]
    for file in mp3_files:
        print('FTPing: ' + file)
        ftp.storbinary('STOR mp3/' + file, open('mp3/' + file, 'rb'))
    print('FTP done, closing connection')
    ftp.close()


def cleanup():
    print('Cleaning up files')
    files = [f for f in os.listdir('downloads') if os.path.isfile(os.path.join('downloads', f))]
    for file in files:
        os.remove('downloads/' + file)
    files = [f for f in os.listdir('mp3') if os.path.isfile(os.path.join('mp3', f))]
    for file in files:
        os.remove('mp3/' + file)


def main():
    if not os.path.isfile('ffmpeg.exe'):
        print('You need the ffmpeg.exe file in the bottom directory to use this program')
        exit()
    config = get_config()
    ftpData = config['FTP']
    host = ftpData['host']
    port = int(ftpData['port'])
    username = ftpData['username']
    password = ftpData['password']
    download()
    convert()
    ftp(host, port, username, password)


if __name__ == "__main__":
   main()