import pandas as pd
import re

# Load artist dataset
artist_data = pd.read_csv(
    "data/spotify_artists_cleaned.csv",
    names=["artist_id", "total_followers", "genres", "name", "artist_popularity"],
)

# Load track dataset
track_data = pd.read_csv(
    "data/spotify_tracks.csv",
    names=[
        "index",
        "track_id",
        "title",
        "artists",
        "explicit",
        "track_popularity",
        "acousticness",
        "danceability",
        "duration_ms",
        "energy",
        "instrumentalness",
        "key",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "time_signature",
        "valence",
    ],
)

# Drop the index column from track data
track_data.drop(columns=["index"], inplace=True)


def split_artists(artist_string):
    # Use regex to split by commas not within quotes
    if artist_string == "artists":
        return artist_string
    artist_string = artist_string.replace("[]", "")
    return re.findall(r"'(.*?)'", artist_string)


# Explode the artists column in track data to have one artist per row
track_data["artists"] = track_data["artists"].apply(split_artists)
track_data_exploded = track_data.explode("artists")

# Merge datasets on artist name
merged_data = pd.merge(
    track_data_exploded, artist_data, left_on="artists", right_on="name", how="left"
).drop(columns=["name"])

# Save the merged dataset to a new CSV file
merged_data.to_csv("data/merged_artist_and_track_data.csv", index=False)
