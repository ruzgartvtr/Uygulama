from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API Bilgileri
SPOTIFY_CLIENT_ID = 'b8f0c956f019488ba3f770f4643e75fe'
SPOTIFY_CLIENT_SECRET = 'e5b4fdb2965e4f03a817f6dbc8c5d403'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = "user-read-playback-state user-modify-playback-state"

# Spotify playlist URL'lerini liste
playlists = [
    "https://open.spotify.com/playlist/0kjhHKjOP2tBLyTBr3vBvG",
    "https://open.spotify.com/playlist/65vGQeUhK8Lu2TDrTVoT1W",
    "https://open.spotify.com/playlist/5wpIJABOsAjziNXu5BPTHV",
    "https://open.spotify.com/playlist/326gAw2zvhUFrt2z7jCBgn",
    "https://open.spotify.com/playlist/3o1E2GmXLiQVVX6TAsoQuo",
    "https://open.spotify.com/playlist/1CSLgeU9aVphYofjeKDVtQ"
]

# Spotipy istemcisi
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
))

# Çalınan şarkılar için bir liste
played_songs = []

class SpotifyRandomPlayer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Başlık
        self.label = Label(text="Spotify Rastgele Çalıcı", font_size=24)
        self.add_widget(self.label)

        # Rastgele çalma düğmesi
        self.play_button = Button(text="Rastgele Şarkı Çal", size_hint=(0.6, 0.2), pos_hint={"center_x": 0.5})
        self.play_button.bind(on_press=self.play_random_song)
        self.add_widget(self.play_button)

        # Durum etiketi
        self.status_label = Label(text="", font_size=18)
        self.add_widget(self.status_label)

    def play_random_song(self, instance):
        try:
            # Rastgele bir playlist seç
            playlist_url = random.choice(playlists)
            playlist_id = playlist_url.split("/")[-1].split("?")[0]

            # Playlist'teki şarkıları al
            tracks = sp.playlist_tracks(playlist_id)['items']
            if not tracks:
                self.status_label.text = "Oynatma listesinde şarkı yok!"
                return

            # Daha önce çalınmayan şarkıları filtrele
            available_tracks = [track for track in tracks if track['track']['uri'] not in played_songs]
            if not available_tracks:
                self.status_label.text = "Tüm şarkılar çalındı!"
                return

            # Rastgele bir şarkı seç ve çal
            random_track = random.choice(available_tracks)
            track_name = random_track['track']['name']
            track_artist = random_track['track']['artists'][0]['name']
            track_uri = random_track['track']['uri']

            sp.start_playback(uris=[track_uri])
            played_songs.append(track_uri)  # Çalınan şarkıyı listeye ekle
            self.status_label.text = f"Çalınıyor: {track_name} - {track_artist}"
        except Exception as e:
            self.status_label.text = f"Hata: {e}"

class SpotifyApp(App):
    def build(self):
        return SpotifyRandomPlayer()

if __name__ == "__main__":
    SpotifyApp().run()
