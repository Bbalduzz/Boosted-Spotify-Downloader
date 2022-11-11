from rich.console import Console
c = Console()
# DL
from mutagen.easyid3 import EasyID3
import os, re
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL
import urllib.request
import ui

client_credentials_manager = SpotifyClientCredentials('1a347b168ca34b2c967e85e733f164c6', 'c6e6ef117c3b426facabb106683cc0bb')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_tracks_id(playlist_id):
	global playlist_name, playlist_owner
	music_id_list = []
	playlist = sp.playlist(playlist_id)
	playlist_name = playlist['name']
	playlist_owner = playlist['owner']['display_name']
	for item in playlist['tracks']['items']:
		music_track = item['track']
		music_id_list.append(music_track['id'])

	return music_id_list, playlist_name

def get_tracks_data(track_id):
	meta = sp.track(track_id)
	track_details = {
		"name": meta['name'],
		"album": meta['album']['name'],
		"artist": meta['album']['artists'][0]['name'],
		"release_date": meta['album']['release_date'],
		"duration": round((meta['duration_ms']*0.001)/60.0, 2)
	}

	return track_details

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f'\rDownloading track... |{bar}| {percent:.2f}%', end='\r')

def my_hook(d):
    if d['status'] == 'downloading':
    	progress_bar(round(float(d['downloaded_bytes'])), float(d['total_bytes']))
    if d['status'] == 'finished':
        c.print('\r ==> [yellow]Downloaded now converting[/yellow]')

def download_track(track):
	try:
		track_name = track['name']
		track_arists = track['artist']
		BASE_URL = f'https://www.youtube.com/results?search_query={track_name}+{track_arists}'.replace(" ", "%20")
		video_ids = re.findall(r"watch\?v=(\S{11})", urllib.request.urlopen(BASE_URL).read().decode())
		yt_url = "https://www.youtube.com/watch?v=" + video_ids[0]
		c.print('[b green]Track found[/b green]: ', track_name, '-', track_arists)
	except Exception as e:
		c.print('[red]ERROR[/red]', e, '==> [red]Failed[/red]')
		pass
	try:
		options = {
			'writethumbnail':True,
		    'format':'bestaudio/best',
		    'postprocessors': [
		    	{'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '320'},
		        {'key': 'EmbedThumbnail'}],
	        'quiet': True,
		    'no_warnings': True,
		   	'outtmpl':f'{playlist_name}/{track_name}.%(ext)s',
		    'progress_hooks': [my_hook],
	    }
		with YoutubeDL(options) as ydl: 
			ydl.download([yt_url])
	except:
		pass

def apply_metadata(track, playlist_name):
	try:
		if '..' not in f'{track["name"]}.mp3':
			song = f'{track["name"]}.mp3'
		else:
			song = f'{track["name"]}mp3'
		metatag = EasyID3(f'{os.getcwd()}/{playlist_name}/{song}')
		metatag['title'] = track['name']
		metatag['artist'] = track['artist']
		metatag['album'] = track['album']
		metatag.RegisterTextKey("track", "TRCK")
		metatag.save()
	except:
		pass

if __name__ == '__main__':
	try:
		c.print(ui.print_banner())
		playlist_id = input('Enter playlist URL:\n')
		infos = get_tracks_id(playlist_id)
		track_ids = infos[0]
		playlist_name = infos[1]
		try:os.mkdir(playlist_name)
		except: pass

		c.print(f'[b red]{playlist_name}[/b red]', 'by', f'[b red]{playlist_owner}', justify='center')
		c.print('Tracks:',len(track_ids), justify='center')

		for i in range(len(track_ids)):
			track = get_tracks_data(track_ids[i])
			print(f'[{i+1}/{len(track_ids)}]', end=' ')
			download_track(track)
			apply_metadata(track, playlist_name)
	except KeyboardInterrupt:
		c.print(ui.leave_msg())
		exit()
