import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

print(CLIENT_ID)
response = requests.get("https://api.thedogapi.com/")
print(response.text)