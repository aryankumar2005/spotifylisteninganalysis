# clean_data.py
# Takes the raw JSON files from my Spotify data export and cleans them
# into one CSV file that I can use for analysis.

import os
import json
import pandas as pd

# Step 1: load all the JSON files 

# Spotify sent my history split across several JSON files, so I loop through
# the folder and add every play from every file into one big list

all_records = []

for filename in os.listdir('data/raw'):
    if filename.endswith('.json'):
        file = open('data/raw/' + filename, encoding='utf-8')   # utf-8 so names like Beyoncé load properly
        records = json.load(file)
        file.close()
        all_records.extend(records)   # extend adds each play to the list (append would add the whole file as one item)

# turn the list into a pandas table (one row per play)
df = pd.DataFrame(all_records)

# save how many rows I started with, so I can check my numbers add up at the end
raw_count = len(df)


# Step 2: fix the timestamps 

# 'ts' is the time each song stopped playing, and Spotify records it in UTC.
# I convert it to UK time so it matches when I was actually listening
# (this handles summer time too, e.g. +1 hour in July but not in December)

df['datetime'] = pd.to_datetime(df['ts'], utc=True)
df['datetime'] = df['datetime'].dt.tz_convert('Europe/London')


# Step 3: rename columns and keep only the ones I need 

# Spotify's column names are long, so I shorten them

df = df.rename(columns={
    'master_metadata_track_name': 'track_name',
    'master_metadata_album_artist_name': 'artist',
    'master_metadata_album_album_name': 'album'
})

# only keep the columns I need for the analysis
# (this also gets rid of personal info like my IP address and username)

columns_to_keep = ['datetime', 'ms_played', 'track_name', 'artist', 'album',
                   'spotify_track_uri', 'reason_start', 'reason_end', 'shuffle', 'skipped']
df = df[columns_to_keep]


# Step 4: remove plays with no track name 

# podcasts and audiobooks don't have a track name, and neither do a few broken records

df = df.dropna(subset=['track_name'])
count_after_missing = len(df)


# Step 5: remove duplicates 

# a duplicate has to have the same end time, the same track and the same duration.
# I don't just use the track, because then it would delete every time I replayed a song

df = df.drop_duplicates(subset=['datetime', 'spotify_track_uri', 'ms_played'])
count_after_duplicates = len(df)


# Step 6: sort and check the numbers add up 

# newest plays first

df = df.sort_values('datetime', ascending=False)

# renumber the rows (removing rows leaves gaps in the numbering)
df = df.reset_index(drop=True)

# check every row I removed is accounted for
print('Raw records:', raw_count)
print('Removed (no track name):', raw_count - count_after_missing)
print('Removed (duplicates):', count_after_missing - count_after_duplicates)
print('Clean records:', count_after_duplicates)


# Step 7: save the clean data 

os.makedirs('data/processed', exist_ok=True)   # make the folder if it doesn't exist yet
df.to_csv('data/processed/spotify_history_clean.csv', index=False)   # index=False so the row numbers aren't saved as a column