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



    def dff(self,playlist_id):
        spotify=self.spotify
        results = spotify.playlist(playlist_id)
        # create a list of song ids
        ids=[]

        for item in results['tracks']['items']:
                track = item['track']['id']
                ids.append(track)
                
        song_meta={'id':[],'album':[], 'name':[], 
                'artist':[],'explicit':[],'popularity':[]}

        for song_id in ids:
            # get song's meta data
            meta = spotify.track(song_id)
            
            # song id
            song_meta['id'].append(song_id)

            # album name
            album=meta['album']['name']
            song_meta['album']+=[album]

            # song name
            song=meta['name']
            song_meta['name']+=[song]
            
            # artists name
            s = ', '
            artist=s.join([singer_name['name'] for singer_name in meta['artists']])
            song_meta['artist']+=[artist]
            
            # explicit: lyrics could be considered offensive or unsuitable for children
            explicit=meta['explicit']
            song_meta['explicit'].append(explicit)
            
            # song popularity
            popularity=meta['popularity']
            song_meta['popularity'].append(popularity)

        song_meta_df=pd.DataFrame.from_dict(song_meta)

        # check the song feature
        features = spotify.audio_features(song_meta['id'])
        # change dictionary to dataframe
        features_df=pd.DataFrame.from_dict(features)

        # convert milliseconds to mins
        # duration_ms: The duration of the track in milliseconds.
        # 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
        features_df['duration_ms']=features_df['duration_ms']/60000

        # combine two dataframe
        final_df=song_meta_df.merge(features_df) 
        print(final_df)
        return final_df
    def __init__(self):
        
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
            })
        

        #convert the response to JSON
        auth_response_data = auth_response.json()

        #save the access token
        access_token = auth_response_data['access_token']
        self.headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        id_dict={'2022':'spotify:playlist:0vXaFFlNzilqtZFXx97G02',
                'HH':'spotify:playlist:0dKeeXOvnBumSstEvUt2tV'}
        
        for id in id_dict.values():
            df=self.dff(playlist_id=id)
        print(df.columns)
        
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