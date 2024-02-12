import os
import shutil
import pandas as pd


df = pd.read_csv('dataset_labels.csv')
csv_filename = 'dataset_encoded.csv'

# Get unique genres
unique_genres = sorted(set(df['genre']))

# Create a column for each genre with default value 0
for genre in unique_genres:
    df[genre] = 0

# Set 1 for the genre column that matches the image's genre
for index, row in df.iterrows():
    df.at[index, row['genre']] = 1

# Drop the 'genre' column as it's no longer needed
df.drop('genre', axis=1, inplace=True)

# Save the updated DataFrame to CSV
df.to_csv(csv_filename, index=False)
