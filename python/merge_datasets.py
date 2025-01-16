import pandas as pd
import re
from difflib import SequenceMatcher

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
# Load billboard charts dataset
billboard_data = pd.read_csv(
    "data/billboard_charts_normalized.csv",
    names=[
        "index",
        "position",
        "title",
        "artists",
        "last week",
        "peak position",
        "weeks on chart",
        "week of",
    ],
)

# Function to split artists in billboard data
billboard_data["artists"] = billboard_data["artists"].apply(split_artists)

# Explode the artists column in billboard data to have one artist per row
billboard_data_exploded = billboard_data.explode("artists")


# Normalize artist names by removing special characters and converting to lowercase
def similar(a, b):
    if pd.isna(a) or pd.isna(b):
        return False
    return SequenceMatcher(None, a, b).ratio() > 0.8

artist_name_map = {}
for artist in merged_data["artists"].unique():
    for billboard_artist in billboard_data_exploded["artists"].unique():
        if similar(artist, billboard_artist):
            artist_name_map[billboard_artist] = artist

# Merge the billboard data with the merged artist and track data on track title and artist name
final_merged_data = pd.merge(
    merged_data,
    billboard_data_exploded,
    left_on=["title", "artists"],
    right_on=["title", "artists"],
    how="left",
)

# Remove duplicates and rows with null values
final_merged_data.drop_duplicates(inplace=True)
final_merged_data.dropna(subset=["position", "artist_id"], inplace=True)

# Sort by the week and position
final_merged_data.sort_values(by=["week of", "position"], inplace=True)

# Save the final merged dataset to a new CSV file
final_merged_data.to_csv("data/final_merged_data.csv", index=False)
