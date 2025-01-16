import pandas as pd
import re

# Load the dataset
file_path = "data/billboard_charts.csv"
billboard_data = pd.read_csv(file_path)


def normalize_artists(artist_str):
    # Split by common delimiters
    delimiters = [
        " Featuring ",
        " featuring ",
        " feat. ",
        " Feat. ",
        " & ",
        " and ",
        " With ",
        " + ",
        " X ",
        " x ",
        " with ",
        " With ",
        " vs. ",
        " Vs. ",
        " vs ",
        " Vs ",
        " / ",
        " duet with ",
        " Duet With ",
        " Duet with ",
        " Presents ",
        " presents ",
        ", ",
    ]
    regex_pattern = "|".join(map(re.escape, delimiters))
    artists = re.split(regex_pattern, artist_str)
    return str(artists)


# Apply the normalization function to the artist column
billboard_data["artist"] = billboard_data["artist"].apply(normalize_artists)

# Save the modified dataset
output_file_path = "data/billboard_charts_normalized.csv"
billboard_data.to_csv(output_file_path, index=False)
