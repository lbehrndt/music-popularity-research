import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load the dataset
final_df = pd.read_csv("./data/final_merged_data.csv")

# Convert 'week of' to datetime and extract the year
final_df["week of"] = pd.to_datetime(final_df["week of"])
final_df["year"] = final_df["week of"].dt.year

# Compute popularity score (100 - position)
final_df["popularity"] = 100 - final_df["position"]

# Define features for regression
features = ["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature", "valence"]

# Store importance values over years
importance_over_years = {feature: [] for feature in features}
years = sorted(final_df["year"].unique())
r2_scores = []

# Perform random forest regression for each year
for year in years:
    yearly_data = final_df[final_df["year"] == year]
    X = yearly_data[features].dropna()
    y = yearly_data["popularity"].loc[X.index]
    
    if len(X) > 10:  # Ensure enough data points for regression
        model = RandomForestRegressor(n_estimators=100, random_state=42)  # 100 trees in the forest
        model.fit(X, y)
        
        # Get feature importances
        importance = model.feature_importances_
        r2_scores.append(r2_score(y, model.predict(X)))
        
        for i, feature in enumerate(features):
            importance_over_years[feature].append((year, importance[i]))

# Plot feature importance over years
for feature, values in importance_over_years.items():
    years, importances = zip(*values)
    plt.figure()
    plt.plot(years, importances, marker='o')
    plt.xlabel("Year")
    plt.ylabel("Importance Value")
    plt.title(f"{feature} Importance Over Years")
    plt.savefig(f"plots/rf/{feature}_importance.png")
    plt.close()

# Plot model accuracy over years
plt.figure()
plt.plot(years, r2_scores, marker='o')
plt.xlabel("Year")
plt.ylabel("R² Score")
plt.title("Random Forest Model Accuracy Over Years")
plt.savefig("plots/rf/model_accuracy.png")
plt.close()

print("Plots saved in 'plots' folder.")
