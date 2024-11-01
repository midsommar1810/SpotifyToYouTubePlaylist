import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="your_spotify_client_id",
    client_secret="your_spotify_client_secret",
    redirect_uri="your_redirect_uri",
    scope="playlist-read-private"))

# YouTube Authentication
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", ["https://www.googleapis.com/auth/youtube"])
credentials = flow.run_local_server(port=0)
youtube = build("youtube", "v3", credentials=credentials)

def get_spotify_playlist(playlist_id):
    # Fetch songs from Spotify
    results = sp.playlist_tracks(playlist_id)
    songs = []
    for item in results['items']:
        track = item['track']
        song = f"{track['name']} {track['artists'][0]['name']}"
        songs.append(song)
    return songs

def create_youtube_playlist(youtube, title="New Playlist", description="Converted from Spotify"):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": "private"},
        },
    )
    response = request.execute()
    return response["id"]

def search_youtube_video(youtube, query):
    # Search for the song on YouTube
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=1
    )
    response = request.execute()
    return response['items'][0]['id']['videoId'] if response['items'] else None

def add_song_to_youtube_playlist(youtube, playlist_id, video_id):
    # Add song to YouTube playlist
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                }
            }
        }
    )
    request.execute()

# Main Flow
spotify_playlist_id = "your_spotify_playlist_id"
songs = get_spotify_playlist(spotify_playlist_id)
youtube_playlist_id = create_youtube_playlist(youtube, title="My Converted Playlist")

for song in songs:
    video_id = search_youtube_video(youtube, song)
    if video_id:
        add_song_to_youtube_playlist(youtube, youtube_playlist_id, video_id)
