import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class SpotifyYouTubeConverter:
    def __init__(self):
        # Spotify Authentication
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="0cdb670e82a943e6b810c5ccd2cf8b9f",
            client_secret="4f6e8d8f791a43049c0efa7b5cf6057b",
            redirect_uri="http://localhost:8888/callback",  # Make sure this matches your registered URI
            scope="playlist-read-private"))

        # YouTube Authentication
        self.youtube = self.authenticate_youtube()

    def authenticate_youtube(self):
        # Set up YouTube authentication
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", ["https://www.googleapis.com/auth/youtube"])
        credentials = flow.run_local_server(port=0)
        return build("youtube", "v3", credentials=credentials)

    def convert_playlist(self, playlist_url):
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        songs = self.get_spotify_playlist(playlist_id)
        youtube_playlist_id = self.create_youtube_playlist(title="My Converted Playlist")

        for song in songs:
            video_id = self.search_youtube_video(song)
            if video_id:
                self.add_song_to_youtube_playlist(youtube_playlist_id, video_id)

    def get_spotify_playlist(self, playlist_id):
        results = self.sp.playlist_tracks(playlist_id)
        songs = []
        for item in results['items']:
            track = item['track']
            song = f"{track['name']} {track['artists'][0]['name']}"
            songs.append(song)
        return songs

    def create_youtube_playlist(self, title="New Playlist", description="Converted from Spotify"):
        request = self.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": title, "description": description},
                "status": {"privacyStatus": "private"},
            },
        )
        response = request.execute()
        return response["id"]

    def search_youtube_video(self, query):
        request = self.youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()
        return response['items'][0]['id']['videoId'] if response['items'] else None

    def add_song_to_youtube_playlist(self, playlist_id, video_id):
        request = self.youtube.playlistItems().insert(
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


if __name__ == "__main__":
    converter = SpotifyYouTubeConverter()
    # Uncomment below for testing purposes if needed
    # converter.convert_playlist("your_spotify_playlist_url")
