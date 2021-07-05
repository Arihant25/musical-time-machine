
import spotipy
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Get the environment variables
load_dotenv(".env")
CLIENT_ID = os.getenv("spotify_client_id")
CLIENT_SECRET = os.getenv("spotify_client_secret")

print("Welcome to Arihant's Music Time Machine!\n")
# Ask the user for the year
date = input(
    "What day do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Split the date into year, month, and day variables
year, month, day = date.split('-')

# Get the html from Billboard for the date entered by the user
html = requests.get(
    f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}")

# Create a BeautifulSoup object with the html data
soup = BeautifulSoup(html.text, 'html.parser')

# Get the song titles from the Hot 100 list
print(f"\nGetting the Hot 100 songs for the date {date}...")
song_titles = [song.text for song in soup.select(
    '.chart-element__information__song')]

# Connect to the Spotify API
auth = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri="http://example.com",
                                   scope="playlist-modify-private")
access_token = auth.get_cached_token()
spotify = spotipy.Spotify(oauth_manager=auth)
user_id = spotify.current_user()["id"]

# Search for each track on Spotify
print("Searching for the songs on Spotify...")
song_uri_list = []
for track in song_titles:
    search = spotify.search(q=f"track:{track}", limit=1, type="track")
    try:
        song_uri_list.append(search["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{track} was not found on Spotify. Skipping...")

# Create a playlist on Spotify
print("Adding the songs to a new Spotify playlist on your account...")
playlist = spotify.user_playlist_create(user_id, f"{date} Billboard Hot 100", public=False,
                                        description=f"These are the songs which were on the Billboard Hot 100 list on {date}.")

# Add the tracks to the playlist
spotify.user_playlist_add_tracks(user_id, playlist["id"], song_uri_list)

print(
    f"Done! Check your Spotify to find the playlist called '{date} Billboard Hot 100'.")
