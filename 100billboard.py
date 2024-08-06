import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth



URL = "https://www.billboard.com/charts/hot-100/2015-11-14/"

response = requests.get(url=URL)
content = response.text

soup = BeautifulSoup(content, "html.parser")

# historical_date = input("Which day of the past year you wanna travel to? type of the date format should be:YYYY-MM-DD: ")
#
# year= historical_date.split("-")[0]
# month= historical_date.split("-")[1]
# date= historical_date.split("-")[2]
# print(year)
# print(month)
# print(date)
song_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_spans]
print(song_names)


spotify_uri = "https://developer.spotify.com/dashboard/create"
Client_id = "ad7f843ebbfc434eac204322d50d0268"
client_secret_key = "bc57cfd03a484a93a315d17ab517bba3"
SCOPE = 'playlist-modify-private playlist-modify-public user-library-read'




sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        redirect_uri=spotify_uri,
        client_id=Client_id,
        client_secret=client_secret_key,
        show_dialog=True,
        cache_path="token.txt",
        username="MEGHANA",
    )
)

user_id = sp.current_user()["id"]


#
# year = "2015"
# for song_name in song_names:
#     query = f"{song_name} year:{year}"
#     results = sp.search(q=query, type='track', limit=1)
#     if results['tracks']['items']:
#         track = results['tracks']['items'][0]
#         print(f"Track: {track['name']}, Artist: {track['artists'][0]['name']}, Spotify URL: {track['external_urls']['spotify']}")
#     else:
#         print(f"Track: {song_name} not found on Spotify")
#


playlist_name = "Billboard Hot 100 - 2015-11-14"
new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
print(f"Created playlist: {new_playlist['name']}")

# Step 4: Search for each song on Spotify and collect track IDs
track_ids = []
year = "2015"
for song_name in song_names:
    query = f"{song_name} year:{year}"
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_ids.append(track['id'])
        print(f"Found: {track['name']} by {track['artists'][0]['name']}")
    else:
        print(f"Track: {song_name} not found on Spotify")

# Step 5: Add tracks to the new playlist
if track_ids:
    sp.playlist_add_items(playlist_id=new_playlist['id'], items=track_ids)
    print(f"Added {len(track_ids)} tracks to the playlist {playlist_name}")
else:
    print("No tracks to add to the playlist.")

