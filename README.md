# Python Data Cleaning: Analysing 228,000 Plays of My Spotify Listening History

## Overview

A project for practising data cleaning and analysis with Python and pandas, using a large, messy, real dataset: my full lifetime Spotify streaming history.

It cleans 228,131 raw play records into 225,311 clean ones, then looks at listening totals, top artists and tracks, and skip behaviour. Most of the work went into cleaning and checking the data before trusting any result.

## Data

- **Source:** Spotify's Extended Streaming History export, requested from my account privacy settings
- **Format:** several JSON files, with one record per play
- **Fields used:** end time of each play, milliseconds played, track, artist, album, track ID, why the play started and ended, shuffle, and whether it was skipped

The raw data contains personal information (IP address, username, device), so it isn't included in this repository.

## Files

- `clean_data.py`: loads the raw JSON files, cleans them and saves one clean CSV
- `basic_stats.py`: listening totals, top artists and tracks, and skip analysis
- `helper.py`: a function that loads the clean CSV, used by the analysis script

## How to run

1. Install pandas: `pip install pandas`
2. Put the Spotify JSON files in a folder called `data/raw/`
3. Run `python clean_data.py`, which creates `data/processed/spotify_history_clean.csv`
4. Run `python basic_stats.py`

## Cleaning

1. **Combine files:** load every JSON file into one table
2. **Fix timestamps:** Spotify records the time each play ended, in UTC. These are converted to UK time, which also handles the switch between GMT and BST
3. **Drop personal fields:** keep only the 10 columns the analysis needs
4. **Remove missing records:** drop podcasts, audiobooks and broken records with no track name
5. **Remove duplicates:** drop records with the same end time, track ID and duration
6. **Reconcile counts:** print the number of records removed at each step, so every row is accounted for

| Step | Records |
|---|---|
| Raw records | 228,131 |
| Removed: no track name | 1,561 |
| Removed: duplicates | 1,259 |
| **Clean records** | **225,311** |

## Data quality checks

**Duplicates.** Before removing them, I checked a sample:

- The duplicate pairs sat next to each other in the raw files, which suggests the same play was logged twice.
- Most were exact copies, clustered in December 2019 and played from another device.
- The rest were zero-length records from app crashes or reloads.

None were real repeat plays.

**The skip flag.** I compared Spotify's `skipped` flag against plays that ended with the forward button. They disagreed on about 23% of records. Breaking it down by year showed why:

| Year | Forward-button plays marked as skipped |
|---|---|
| 2018–2021 | 0% |
| 2022 | 7% |
| 2023 onwards | 100% |

So the flag wasn't recorded before 2023. Its "False" values in earlier years mean *missing*, not *not skipped*. Skip analysis therefore only uses plays from 2023 onwards (140,346 plays), and excludes zero-length plays.

## Results

- **6,848 hours** of listening (about 285 days) across 4,670 artists and 13,778 songs
- **Top artist:** Kanye West, at 383 hours
- **Top track:** *After Party* by Don Toliver, at 408 plays
- **Overall skip rate (2023 onwards): 62%**
- **Usual taste vs everything else:** I skipped artists outside my top 50 **65%** of the time, against **58%** for my top 50
- The most-skipped artists (95–100% skip rate) are almost all outside my usual taste. This suggests they reached me through playlists or autoplay rather than by choice

## Limitations

- **Short plays:** the skip rate includes short plays, because most skips happen in the first 30 seconds. Listening totals only count plays over 30 seconds, which matches Spotify's definition of a stream.
- **Recent data only:** skip results only cover 2023 onwards.
