## Project Progress Timeline

### Data Collection

We started by scraping weekly Billboard chart data from January 2, 2010, to November 16, 2024, saving it as `billboard_charts.csv`. Next, we retrieved track and artist data via Spotify’s API, saved separately as `spotify_tracks.csv` and `spotify_artists.csv` for better organization.

---

### Data Normalization and Merging

Billboard listed artists differently than Spotify (e.g., "Kesha featuring Adele" vs. `['Ke$ha', 'Adele']`). We normalized names into arrays, standardizing formats and reducing inconsistencies. Some data loss occurred during normalization and merging, but this was acceptable given the dataset’s size. The final merged dataset includes ~50,000 entries, down from 75,000 Billboard entries, providing high-quality data for analysis.

---

### Individual Dataset Usage

The original datasets remain useful for specific tasks. For example, our `unique_songs_per_year_bar_chart` visualization relied solely on `billboard_charts.csv`, as it didn’t require Spotify data. We documented each dataset used to ensure clarity and transparency.

---

### Audio Features

We retrieved various audio features for each track using Spotify’s API ([More Info](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)). These features are analyzed to understand how the sound characteristics of popular songs have evolved over time.


| **Audio Feature**      | **Description**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| **Track Popularity**    | Measures the popularity of a track on a scale from 0 to 100.                     |
| **Acousticness**        | Indicates the likelihood that a track is purely acoustic, with values between 0 and 1. |
| **Danceability**        | Reflects how suitable a track is for dancing, ranging from 0 (least) to 1 (most). |
| **Duration (ms)**       | The length of the track in milliseconds, providing insight into song duration trends. |
| **Energy**              | Measures the intensity and activity of a track, from 0 (low) to 1 (high).       |
| **Instrumentalness**    | Indicates whether a track is instrumental, ranging from 0 (not) to 1 (instrumental). |
| **Key**                 | Represents the musical key of the track (e.g., 0 for C major).                 |
| **Liveness**            | Measures the presence of a live audience in the track, from 0 (not live) to 1 (live). |
| **Loudness**            | Reflects the overall loudness of the track in decibels (dB).                   |
| **Speechiness**         | Measures the presence of spoken words in the track, from 0 (no speech) to 1 (mostly speech). |
| **Tempo**               | The track’s beats per minute (BPM), indicating the pace of the song.           |
| **Valence**             | Indicates the positivity or negativity of the track, ranging from 0 (negative) to 1 (positive). |
