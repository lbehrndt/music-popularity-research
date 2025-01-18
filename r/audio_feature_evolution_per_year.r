# Load necessary libraries
library(tidyverse)
library(scales)

# Load the dataset
data <- read_csv("data/final_merged_data.csv")

# Convert the 'week of' column to Date type and extract the year
data <- data %>%
  mutate(
    week_of = as.Date(`week of`, format = "%Y-%m-%d"),
    year = as.integer(format(week_of, "%Y")) # Ensure year is numeric
  )

# List of audio features
audio_features <- c(
  "acousticness", "danceability", "duration_ms",
  "energy", "liveness", "loudness", "speechiness", "tempo", "valence"
)

# Normalize the audio features
data <- data %>%
  mutate(across(all_of(audio_features), rescale))

# Melt the dataset to long format for ggplot2
data_long <- data %>%
  select(year, all_of(audio_features)) %>%
  pivot_longer(cols = -year, names_to = "feature", values_to = "value")

# Check for missing or non-numeric values in 'value' column
data_long <- data_long %>%
  filter(!is.na(value)) # Remove rows with missing values in 'value'

# Calculate the median of each feature per year
data_median <- data_long %>%
  group_by(year, feature) %>%
  summarize(median_value = median(value, na.rm = TRUE), .groups = "drop")

# Plot the evolution of each audio feature per year (using median)
plot <- ggplot(data_median, aes(x = year, y = median_value, color = feature, group = feature)) +
  geom_line() +
  labs(
    title = "Evolution of Audio Features per Year (Median)",
    x = "Year",
    y = "Median Normalized Value",
    color = "Audio Feature"
  )

# Save the plot as a PNG file
ggsave(filename = paste0("plots/", "audio_feature_median_evolution_per_year.png"), plot = plot)
