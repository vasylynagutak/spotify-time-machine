import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
song_name = ["The list of song", "titles from your", "web scrape"]
URL = ("https://www.billboard.com/charts/hot-100/" + date)

CLIENT_ID = "739c1ba1f9e4474fa593bf91d4902743"
CLIENT_SECRET = "b762dcd5586c47d2ad76e0649665e29d"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
song_names_span = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_span]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
