# Python Data Cleaning: Analysing 228,000 Plays of My Spotify Listening History

## Overview

I wanted to practise data cleaning in Python on a big, real dataset, so I requested my full Spotify listening history and taught myself pandas to work with it.

The raw export had 228,131 plays. After cleaning I had 225,311, which I used to look at my listening totals, top artists and tracks, and how often I skip songs. Most of my time went on the cleaning, because I found a few problems in the data that would have given me wrong results if I'd ignored them.

## Data

The data is Spotify's Extended Streaming History export, which you can request from your account's privacy settings. It comes as several JSON files with one record for every play, including when the play ended, how long it lasted, the track and artist, why it started and ended, and whether it was skipped.

The raw files include personal information like my IP address and username, so I haven't uploaded them.

## Files

- `clean_data.py` loads the raw JSON files, cleans them and saves one CSV
- `basic_stats.py` works out the listening totals, top artists and tracks, and skip rates
- `helper.py` has a function to load the clean CSV

## How to run

1. Install pandas with `pip install pandas`
2. Put the Spotify JSON files in a folder called `data/raw/`
3. Run `python clean_data.py` (this creates `data/processed/spotify_history_clean.csv`)
4. Run `python basic_stats.py`

## Cleaning

1. Load all the JSON files into one table
2. Convert the timestamps from UTC to UK time, so they line up with when I was actually listening (this also handles the switch between GMT and BST)
3. Keep only the 10 columns I need, which also gets rid of the personal data
4. Remove records with no track name (mostly podcasts, plus a few broken records)
5. Remove duplicates, meaning records with the same end time, track ID and duration. I didn't match on track alone, or it would have deleted every time I replayed a song
6. Print how many records were removed at each step, to check everything adds up

| Step | Records |
|---|---|
| Raw records | 228,131 |
| No track name | -1,561 |
| Duplicates | -1,259 |
| Clean records | 225,311 |

## Checking the data

### Duplicates

Before removing the duplicates I looked at a sample of them. The pairs were right next to each other in the raw files, so it looks like Spotify logged the same play twice. Most were exact copies from December 2019, all played from another device. The rest were zero-length records from things like the app crashing. None of them were real repeat plays.

### The skip flag

When I compared Spotify's `skipped` column with plays that ended with the forward button, they disagreed on about 23% of records. Splitting it by year showed why:

| Year | Forward-button plays marked as skipped |
|---|---|
| 2018–2021 | 0% |
| 2022 | 7% |
| 2023 onwards | 100% |

Spotify just didn't record skips before 2023, so "False" in the older data means the information is missing, not that I didn't skip. Because of this, I only used plays from 2023 onwards (140,346 plays) for the skip analysis, and left out zero-length plays.

## Results

- 6,848 hours of listening (about 285 days) across 4,670 artists and 13,778 songs
- My top artist was Kanye West, at 383 hours
- My top track was After Party by Don Toliver, at 408 plays, although a lot of those came from it being left on repeat on my Xbox by accident
- Since 2023, I've skipped 62% of plays overall
- I skipped artists outside my top 50 65% of the time, compared with 58% for my top 50
- Nearly all of my most-skipped artists (95–100% skip rate) are ones I don't normally listen to, so they probably came up through playlists or autoplay

## Limitations

- The skip rate includes short plays, because most skips happen in the first 30 seconds. The listening totals only count plays over 30 seconds, the same rule Spotify uses for counting a stream.
- The skip results only cover 2023 onwards.
