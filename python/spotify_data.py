import base64
import os
import sys
import time
import requests
from dotenv import load_dotenv
import csv

BASE_URL = "https://api.spotify.com/v1"
ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
ACCESS_TOKEN_EXPIRATION = 3600  # 1 hour
RATE_LIMIT = 25
FETCHED_TRACKS = 0
FETCHED_ARTIST = 0


class SpotifyTokenManager:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = ACCESS_TOKEN_URL
        self.expiry_time = time.time() + ACCESS_TOKEN_EXPIRATION
        self.access_token = None

    def initialize_token(self):
        self.access_token = self.refresh_access_token()

    def refresh_access_token(self):
        print("Fetching new token...")

        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(ACCESS_TOKEN_URL, headers=headers, data=data)
        if response.status_code != 200:
            response.raise_for_status()

        data = response.json()
        self.access_token = data.get("access_token")
        self.expiry_time = time.time() + ACCESS_TOKEN_EXPIRATION
        print("New token fetched: ", self.access_token)
        return self.access_token

    def get_token(self):
        if time.time() >= self.expiry_time:
            self.access_token = self.refresh_access_token()
        return self.access_token


def get_unique_tracks(tracks: list[tuple]) -> list[tuple]:
    seen = set()
    unique_tracks = []
    for track in tracks:
        if track not in seen:
            seen.add(track)
            unique_tracks.append(track)

    print(f"Found {len(unique_tracks)} unique tracks")
    return unique_tracks


def read_csv(filename: str) -> list:
    print(f"Reading {filename}...")
    data = []
    with open(filename, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


def get_credentials():
    load_dotenv()

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        print(
            "Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your .env file"
        )
        sys.exit(1)

    return client_id, client_secret


def save_to_csv(filename, data: list):
    if not data:
        print(f"No data to save for {filename}")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def fetch_track_data(track_ids, token_manager):
    global FETCHED_TRACKS
    headers = {"Authorization": f"Bearer {token_manager.get_token()}"}
    track_url = f"{BASE_URL}/tracks"
    audio_features_url = f"{BASE_URL}/audio-features"

    track_response = requests.get(
        track_url, headers=headers, params={"ids": ",".join(track_ids)}
    )
    if track_response.status_code != 200:
        track_response.raise_for_status()

    audio_features_response = requests.get(
        audio_features_url, headers=headers, params={"ids": ",".join(track_ids)}
    )
    if audio_features_response.status_code != 200:
        audio_features_response.raise_for_status()

    try:
        tracks = track_response.json().get("tracks", [])
        audio_features = audio_features_response.json().get("audio_features", [])
        track_data = []
        for track, features in zip(tracks, audio_features):
            FETCHED_TRACKS += 1
            track_data.append(
                {
                    "index": FETCHED_TRACKS,
                    "track_id": track.get("id"),
                    "title": track.get("name"),
                    "artists": [artist.get("name") for artist in track.get("artists")],
                    "explicit": track.get("explicit"),
                    "track_popularity": track.get("popularity"),
                    "acousticness": features.get("acousticness"),
                    "danceability": features.get("danceability"),
                    "duration_ms": features.get("duration_ms"),
                    "energy": features.get("energy"),
                    "instrumentalness": features.get("instrumentalness"),
                    "key": features.get("key"),
                    "liveness": features.get("liveness"),
                    "loudness": features.get("loudness"),
                    "mode": features.get("mode"),
                    "speechiness": features.get("speechiness"),
                    "tempo": features.get("tempo"),
                    "time_signature": features.get("time_signature"),
                    "valence": features.get("valence"),
                }
            )
        return track_data
    except:
        print(f"Error parsing track data.")
        return []


def fetch_artist_data(artist_ids, token_manager):
    global FETCHED_ARTIST
    headers = {"Authorization": f"Bearer {token_manager.get_token()}"}
    url = f"{BASE_URL}/artists"

    response = requests.get(url, headers=headers, params={"ids": ",".join(artist_ids)})
    if response.status_code != 200:
        response.raise_for_status()

    try:
        artists = response.json().get("artists", [])
        artist_data = []
        for artist in artists:
            FETCHED_ARTIST += 1
            artist_data.append(
                {
                    "index": FETCHED_ARTIST,
                    "artist_id": artist.get("id"),
                    "total_followers": artist.get("followers").get("total"),
                    "genres": artist.get("genres"),
                    "name": artist.get("name"),
                    "artist_popularity": artist.get("popularity"),
                }
            )
        return artist_data
    except:
        print(f"Error parsing artist data.")
        return []


def fetch_data(track: tuple, token_manager):
    title, artist = track
    headers = {"Authorization": f"Bearer {token_manager.get_token()}"}
    params = {
        "q": f"{title} {artist}",
        "type": "track,artist",
        "market": "US",
        "limit": 1,
    }
    url = f"{BASE_URL}/search"

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        response.raise_for_status()

    data = response.json()
    try:
        track_id = data.get("tracks", {}).get("items", [{}])[0].get("id", None)
        artist_id = data.get("artists", {}).get("items", [{}])[0].get("id", None)
        if track_id is None or artist_id is None:
            raise ValueError("Received None value for track_id or artist_id")

        return track_id, artist_id
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error fetching ids: {e}")
        return None, None


def process_data(tracks, token_manager: SpotifyTokenManager):
    print(f"Processing {len(tracks)} tracks...")

    retries = 5
    delay = 1
    track_ids = []
    artist_ids = []
    track_data = []
    artist_data = []

    for i, raw_track in enumerate(tracks):
        for attempt in range(retries):
            try:
                track_id, artist_id = fetch_data(raw_track, token_manager)
                if track_id and artist_id:
                    track_ids.append(track_id)
                    artist_ids.append(artist_id)
                print(f"{i+1}/{len(tracks)} ids processed")
                break

            except requests.exceptions.RequestException as e:
                print(f"Error fetching track_ids: {type(e).__name__} - {e}")

                if e.response.status_code == 429:
                    wait_time = delay * (2**attempt)
                    print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    delay = min(delay * 2, 60)
                else:
                    break

        if len(track_ids) >= 50:
            track_data.extend(fetch_track_data(track_ids, token_manager))
            artist_data.extend(fetch_artist_data(artist_ids, token_manager))
            print(f"{len(track_data)}/{len(tracks)} track data processed")
            print(f"{len(artist_data)}/{len(tracks)} artist data processed")
            track_ids = []
            artist_ids = []
            print("Sleep for 10 seconds Zzz....")
            time.sleep(10)  # wait 10 seconds before fetching more data

    if track_ids:
        track_data.extend(fetch_track_data(track_ids, token_manager))
        artist_data.extend(fetch_artist_data(artist_ids, token_manager))

    print(f"Processed {len(track_data)} tracks and {len(artist_data)} artists")
    return track_data, artist_data


def main():
    csv_data = read_csv("repo/billboard_charts.csv")
    raw_tracks = [(row["title"], row["artist"]) for row in csv_data]
    unique_tracks = get_unique_tracks(raw_tracks)

    client_id, client_secret = get_credentials()
    token_manager = SpotifyTokenManager(client_id, client_secret)
    token_manager.initialize_token()

    track_data, artist_data = process_data(unique_tracks, token_manager)

    save_to_csv("spotify_tracks.csv", track_data)
    save_to_csv("spotify_artists.csv", artist_data)


if __name__ == "__main__":
    main()
