import os
import shutil
import pandas as pd

source_dir = 'dataset'  # Your existing dataset directory
target_dir = 'dataset4'  # New directory where all images will be moved
csv_filename = 'dataset_labels.csv'  # CSV file to store labels

# Create the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Initialize a list to store CSV data
csv_data = []

# List all genre directories
genres = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

for genre in genres:
    genre_dir = os.path.join(source_dir, genre)
    for img_filename in os.listdir(genre_dir):
        if img_filename.endswith(('.jpg', '.jpeg', '.png')):  # Check for image files
            # New filename with genre prefix
            new_filename = f"{genre}_{img_filename}"
            
            # Move and rename image file
            shutil.move(os.path.join(genre_dir, img_filename), os.path.join(target_dir, new_filename))
            
            # Prepare data for CSV
            csv_data.append({'filename': new_filename, 'genre': genre})

# Convert the list to a DataFrame
df = pd.DataFrame(csv_data)

# Save to CSV file
df.to_csv(csv_filename, index=False)
