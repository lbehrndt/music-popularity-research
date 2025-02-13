# Audio Features Effect On Listening Trends Research Repository 

## Our Motivation
Music trends shift due to various factors, including technological advancements, audience preferences, and industry strategies. A wealth of data on song popularity and individual tracks is available online. Additionally, key audio features such as tempo, duration, and valence influence a song's appeal. With this project, we aimed to explore these trends through data analysis, identifying patterns that shape the future of popular music by examining the role of musical features in driving appeal.

## Research Question
This repository contains the code for our research question "How do musical characteristics affect the popularity of songs over time, and whether or not COVID has influenced this?", which explores various scripts to generate insightful plots and graphs to support this question.

## Visualization
![image](https://github.com/user-attachments/assets/5dcf918b-9de6-4dfe-8481-68eef655fd74) 

The graph above illustrates how the correlation between different musical features and popularity has evolved over time. (2010–2024).

For a deeper analysis, check out our presentation: https://docs.google.com/presentation/d/1oPbIgviwv0gNkZu2t5OfWKfuZmfNWo22DO01aFbaS2M/edit?pli=1#slide=id.p

## Getting Started

### Cloning the Repository
To download the project, use the following command:
```sh
git clone https://github.com/lbehrndt/music-popularity-research.git
cd music-popularity-research
```

### [OPTIONAL] Creating a Spotify API account

> You only need to do this if you want to scrape the data yourself.

1. Go to Spotifys Web [Spotify's Web API](https://developer.spotify.com/) and follow the steps to get started.

2. After creating an account, create a `.env` file from the `.env.example`:
```env
SPOTIFY_CLIENT_ID=YOUR_ID
SPOTIFY_CLIENT_SECRET=YOUR_SECRET
```

3. Paste in your credentials as described on Spotify.

### Running Python Scripts
Ensure you have Python 3 installed. Install dependencies using:
```sh
pip install -r requirements.txt
```
To run an individual Python script, use:
```sh
python path/to/script.py
```

### Running R Scripts
Ensure you have R installed along with necessary packages (tidyverse, scales). You can install dependencies in R using:
```r
install.packages("tidyverse")
```
To run an individual R script, use:
```sh
Rscript path/to/script.R
```

## Project Structure
```
📂 MUSIC-POPULARITY-RESEARCH
├── 📂 data            # Contains datasets
├── 📂 plots           # Contains generated plots
├── 📂 python          # Contains Python Scripts
├── 📂 r               # Contains R scripts
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```
