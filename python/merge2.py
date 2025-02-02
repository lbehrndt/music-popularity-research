import pandas as pd

# Load the datasets
spotify_df = pd.read_csv("./data/spotify_tracks.csv")
billboard_df = pd.read_csv("./data/billboard_charts_normalized.csv")

# Compute popularity score (100 - position)
billboard_df["popularity"] = 100 - billboard_df["position"]

# Keep only the highest ranked (smallest position) entry per title in Billboard
billboard_df = billboard_df.sort_values("position").drop_duplicates(subset="title", keep="first")

# Merge the two datasets on 'title'
merged_df = pd.merge(spotify_df, billboard_df, on="title", how="outer")

# Save the merged dataset
merged_df.to_csv("./data/merged_tracks.csv", index=False)

print("Merged dataset saved to ./data/merged_tracks.csv")
