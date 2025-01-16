library(tidyverse)

data <- read_csv("data/billboard_charts.csv")

# Ensure the 'week of' column is in Date format
data <- data %>%
    mutate(`week of` = as.Date(`week of`, format="%Y-%m-%d"))

# Extract the year from the 'week of' column
data <- data %>%
    mutate(year = format(`week of`, "%Y"))

# Identify unique songs per year
unique_songs_per_year <- data %>%
    select(year, title, artist) %>%
    distinct(title, artist, .keep_all = TRUE) %>%
    group_by(year) %>%
    summarise(unique_songs = n())

# Print the result
print(unique_songs_per_year)

# Save the result to a CSV file
write_csv(unique_songs_per_year, "data/unique_songs_per_year.csv")

# Create a bar chart
ggplot(unique_songs_per_year, aes(x = year, y = unique_songs)) +
    geom_bar(stat = "identity") +
    labs(title = "Unique Songs Per Year", x = "Year", y = "Number of Unique Songs") +
    theme_minimal()

# Save the bar chart to a file
ggsave("plots/unique_songs_per_year_bar_chart.png")