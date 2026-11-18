# basic_stats.py
# Works out my listening totals, top artists and tracks, and skip rates from the clean data

import pandas as pd
from helper import load_data

df = load_data()


# Listening totals 

# Spotify only counts a play as a 'stream' if it lasts more than 30 seconds,
# so I use the same rule here so accidental taps don't count
listens = df[df['ms_played'] > 30000]

# ms_played is in milliseconds, so divide by 1000 for seconds, 60 for minutes, 60 for hours
total_hours = listens['ms_played'].sum() / 1000 / 60 / 60
print('Total hours listened:', round(total_hours, 1))

print('Different artists:', listens['artist'].nunique())
print('Different songs:', listens['track_name'].nunique())


# Top artists and tracks

# add up the listening time for each artist (like a pivot table in Excel)
artist_time = listens.groupby('artist')['ms_played'].sum()
artist_hours = artist_time / 1000 / 60 / 60
top_artists = artist_hours.sort_values(ascending=False).head(10)
print('\nTop 10 artists (hours):')
print(top_artists.round(1))

# count how many times I played each song
# (I group by track AND artist because different artists can have songs with the same name)
track_plays = listens.groupby(['track_name', 'artist']).size()
top_tracks = track_plays.sort_values(ascending=False).head(20)
print('\nTop 20 tracks (plays):')
print(top_tracks)


# Skip analysis

# I found that Spotify didn't record the 'skipped' column properly before 2023
# (it almost always said False, even when I pressed the forward button),
# so I only use plays from 2023 onwards
df['year'] = df['datetime'].dt.year
skip_plays = df[df['year'] >= 2023]

# remove plays that lasted 0 milliseconds - these are things like the app crashing, not real plays
skip_plays = skip_plays[skip_plays['ms_played'] > 0]

# I DON'T use the 30 second rule here, because most skips happen in the first 30 seconds,
# so I would lose most of the skips

# .copy() makes it a separate table, so adding a column later doesn't cause a warning
skip_plays = skip_plays.copy()

print('\nPlays used for skip analysis (2023 onwards):', len(skip_plays))

# skip rate for each artist
# (skipped is True or False, and the mean of True/False is the fraction that are True)
skip_rate = skip_plays.groupby('artist')['skipped'].mean()
play_count = skip_plays.groupby('artist').size()

# put them side by side in one table
skip_table = pd.DataFrame({'skip_rate': skip_rate, 'plays': play_count})

# only include artists with at least 20 plays, otherwise an artist with 1 play
# that I skipped would show up as a 100% skip rate
skip_table = skip_table[skip_table['plays'] >= 20]

most_skipped = skip_table.sort_values('skip_rate', ascending=False).head(10)
print('\nMost skipped artists (at least 20 plays):')
print(most_skipped.round(2))


# Do I skip artists outside my usual taste more?

# my 'usual taste' = my top 50 artists by total listening time
top_50_artists = artist_hours.sort_values(ascending=False).head(50).index

# True if the artist is in my top 50, False if not
skip_plays['in_top_50'] = skip_plays['artist'].isin(top_50_artists)

# compare the skip rate for the two groups
print('\nSkip rate: top 50 artists (True) vs everyone else (False)')
print(skip_plays.groupby('in_top_50')['skipped'].mean().round(3))
print(skip_plays.groupby('in_top_50').size())
