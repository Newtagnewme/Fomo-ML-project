import os
import shutil
import pandas as pd


source_dir = 'dataset'  
target_dir = 'dataset4'  
csv_filename = 'dataset_labels.csv' 
IMGEXTENSIONS = ('.jpg', '.jpeg', '.png')

# encode_genre_to_csv('dataset_labels.csv', 'dataset_encoded.csv')
def encode_genre_to_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    unique_genres = sorted(set(df['genre']))

    for genre in unique_genres:
        df[genre] = 0

    for index, row in df.iterrows():
        df.at[index, row['genre']] = 1

    df.drop('genre', axis=1, inplace=True)
    df.to_csv(output_csv, index=False)


# move_and_encode_images(source_dir, target_dir, csv_filename)
def move_and_encode_images(source_dir, target_dir, csv_filename):
    os.makedirs(target_dir, exist_ok=True)
    csv_data = []
    # List all genre directories
    genres = [
        d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))
    ]
    for genre in genres:
        genre_dir = os.path.join(source_dir, genre)
        for img_filename in os.listdir(genre_dir):
            if img_filename.endswith(IMGEXTENSIONS): 
                new_filename = f"{genre}_{img_filename}"
                # rename file
                shutil.move(os.path.join(genre_dir, img_filename), os.path.join(target_dir, new_filename))                
                # CSV
                csv_data.append({'filename': new_filename, 'genre': genre})

    df = pd.DataFrame(csv_data)
    # Save to CSV file
    df.to_csv(csv_filename, index=False)

