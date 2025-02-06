# Load necessary libraries
library(tidyverse)

# Load the dataset
data <- read_csv("data/final_merged_data.csv")

# Convert the 'week of' column to Date type and extract the year
data <- data %>%
    mutate(
        week_of = as.Date(`week of`, format = "%Y-%m-%d"),
        year = format(week_of, "%Y")
    )

# List of audio features to plot
audio_features <- c(
    "track_popularity", "acousticness", "danceability", "duration_ms",
    "energy", "instrumentalness", "key", "liveness", "loudness", "speechiness", "tempo", "valence"
)

# Create a box plot for each audio feature per year
for (feature in audio_features) {
    p <- ggplot(data, aes(x = year, y = .data[[feature]])) +
        geom_boxplot(fill = "blue") +
        labs(
            title = paste("Distribution of", feature, "per Year"),
            x = "Year",
            y = feature
        ) +
        theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
        theme(legend.position = "none")

    # Save the plot
    ggsave(filename = paste0("plots/distribution/", feature, "_distribution_per_year.png"), plot = p)
}
