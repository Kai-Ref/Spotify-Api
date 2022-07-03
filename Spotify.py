import requests
import os
import spotipy
import sys
import pandas as pd
import seaborn as sns
import base64
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'


#Client Credentials Flow
class Spotify():
    def __init__(self):
        
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
            })

        self.spotify.current_playback()
        #convert the response to JSON
        auth_response_data = auth_response.json()

        #save the access token
        access_token = auth_response_data['access_token']
        self.headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}


        tracks=[]
        for i in range(len(id)):
            track=getTrackFeatures(self.spotify,id[i])
            tracks.append(track)
        print(tracks)

        artists=['Drake','Taylor Swift']
        for artist in artists:
            result = self.spotify.search(artist) #search query
            artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
            select_artist = self.spotify.artist(artist_uri)['name']
            print(select_artist)

        id=getTrackID(self.spotify,'11146658800','0vXaFFlNzilqtZFXx97G02')

    def getTrackID(spotify,user,playlist_id):
        id=[]
        play_list=spotify.user_playlist(user,playlist_id)
        for item in play_list['tracks']['items']:
            track = item['track']
            id.append(track['id'])
        return id
        

    def getTrackFeatures(spotify,id):
        meta=spotify.track(id)
        features= spotify.audio_features(id)

        name=meta['name']
        album=meta['album']['name']

        track=[name,album]
        return track


    def getTop():
        scope = 'user-top-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        ranges = ['short_term', 'medium_term', 'long_term']

        for sp_range in ranges:
            print("range:", sp_range)
            results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            for i, item in enumerate(results['items']):
                print(i, item['name'], '//', item['artists'][0]['name'])
            print()

    def getSavedTracks():
        #Authorization Code Flow
        scope = "user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        
        results = self.sp.current_user_saved_tracks()
        print(results)
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])





def main():
    service = Spotify()

if __name__ == '__main__':
    main()