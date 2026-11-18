# helper.py
# A function to load my cleaned Spotify data, so I don't have to repeat
# the same loading code in every analysis script.

import pandas as pd


def load_data():
    # read the clean CSV that clean_data.py made
    df = pd.read_csv('data/processed/spotify_history_clean.csv')

    # the dates come back from the CSV as text, so turn them back into dates
    # (some are +00:00 for winter and some are +01:00 for summer, so I read them
    # all as UTC first and then convert back to UK time)
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    df['datetime'] = df['datetime'].dt.tz_convert('Europe/London')

    return df