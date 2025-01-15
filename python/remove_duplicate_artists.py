import pandas as pd

def remove_duplicate_artists(input_csv, output_csv):
    # Read the CSV file without the index column
    df = pd.read_csv(input_csv, index_col=False)
    
    # Remove the 'index' column if it exists
    if 'index' in df.columns:
        df = df.drop(columns=['index'])
    
    # Remove duplicate artists
    df_cleaned = df.drop_duplicates(subset='artist_id')
    
    # Save the cleaned data to a new CSV file
    df_cleaned.to_csv(output_csv, index=False)

# Example usage
input_csv = '/Users/leon.behrndt/Desktop/personal/Studium/Semester 5/TU/research/music-popularity-research/artist_data/spotify_artists.csv'
output_csv = '/Users/leon.behrndt/Desktop/personal/Studium/Semester 5/TU/research/music-popularity-research/artist_data/spotify_artists_cleaned.csv'
remove_duplicate_artists(input_csv, output_csv)