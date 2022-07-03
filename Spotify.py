import requests
import os
import spotipy
import sys
import pandas as pd
import seaborn as sns
import base64
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
auth_response = requests.post(AUTH_URL, {
'grant_type': 'client_credentials',
'client_id': CLIENT_ID,
'client_secret': CLIENT_SECRET,
    })

print(CLIENT_ID)
response = requests.get("https://api.thedogapi.com/")
print(response.text)