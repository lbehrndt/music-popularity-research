# Data Science with Python and R

This repository contains the code for our research question "How do musical characteristics affect the popularity of songs over time, and whether or not COVID has influenced this?", which explores various scripts to generate insightful plots and graphs to support this question.

## Getting Started

### Cloning the Repository
To download the project, use the following command:
```sh
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### Creating a Spotify API account

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
