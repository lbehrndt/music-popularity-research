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

### Summary

- **Data Collection:** Scraped Billboard data (2010-2024) and retrieved Spotify track and artist data.
- **Normalization:** Standardized artist names across datasets, minimizing inconsistencies.
- **Merging:** Consolidated datasets into ~50,000 high-quality entries.
- **Analysis:** Used original datasets for specific visualizations, ensuring clear documentation and reproducibility.

