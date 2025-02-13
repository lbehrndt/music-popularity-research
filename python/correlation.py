import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("plots/tt", exist_ok=True)

# Load dataset
data = pd.read_csv('./data/final_merged_data.csv')

# Selecting relevant columns for correlation with popularity
features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
target = 'popularity'

# Calculate correlations
correlations = data[features + [target]].corr()

# Plot correlation with popularity (track_popularity)
correlation_popularity = correlations[target].drop(target)  # Remove self-correlation
plt.figure(figsize=(10, 6))
sns.lineplot(x=correlation_popularity.index, y=correlation_popularity.values, marker='o')
plt.title('Correlation with Popularity (Track Popularity)')
plt.xlabel('Feature')
plt.ylabel('Correlation')
plt.xticks(rotation=45)
plt.tight_layout()

# Save plot to the specified folder
plt.savefig('plots/tt/correlation_popularity.png')
plt.close()

# For the evolution of correlation over years
# Extract year from 'week of' column (assuming it is in 'YYYY-MM-DD' format)
data['year'] = pd.to_datetime(data['week of']).dt.year

# Group by year and calculate average correlation for each feature
yearly_correlations = []
for year in data['year'].unique():
    yearly_data = data[data['year'] == year]
    correlations_year = yearly_data[features + [target]].corr()
    yearly_correlations.append(correlations_year[target].drop(target))  # Only save correlation with popularity

# Create a dataframe for the evolution of correlation over years
evolution_df = pd.DataFrame(yearly_correlations, index=data['year'].unique(), columns=features)

# Plot evolution of correlation over years
plt.figure(figsize=(12, 8))
for feature in features:
    plt.plot(evolution_df.index, evolution_df[feature], label=feature, marker='o')

plt.title('Evolution of Correlation with Popularity Over Years')
plt.xlabel('Year')
plt.ylabel('Correlation')
plt.legend(title='Feature')
plt.tight_layout()

# Save the plot for evolution of correlation
plt.savefig('plots/tt/evolution_of_correlation.png')
plt.close()

print("Plots saved in 'plots/tt' folder.")