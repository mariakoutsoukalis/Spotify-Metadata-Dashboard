import spotipy #Library for the Spotify API Requests
from spotipy.oauth2 import SpotifyClientCredentials #Spotipy.oauth2 Module with client credentials class - Authenticate and make requests to the Spotify API without user authorization
import pandas as pd
from credentials import client_id, client_secret #Client Credentials from developer.spotify.com
from time import sleep #Module to elicit delays during API request to avoid hitting rate limits/timeout when processing data

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""Function to retrieve the track Metadata"""

def retrieve_track_data(song_ids, batch_size=10):
    song_meta = dict(id=[], acousticness=[], danceability=[], energy=[], instrumentalness=[], key=[],
                     liveness=[], loudness=[], speechiness=[], tempo=[], time_signature=[], valence=[])
    for i in range(0, len(song_ids), batch_size):
        batch = song_ids[i:i + batch_size]
        try:
            #audio_features is a method that initializes the authentication details.
            meta = sp.audio_features(batch)
            for song in meta:
                if song:  # Check if song is not None
                    song_meta['id'].append(song['id'])
                    song_meta['acousticness'].append(song['acousticness'])
                    song_meta['danceability'].append(song['danceability'])
                    song_meta['energy'].append(song['energy'])
                    song_meta['instrumentalness'].append(song['instrumentalness'])
                    song_meta['key'].append(song['key'])
                    song_meta['liveness'].append(song['liveness'])
                    song_meta['loudness'].append(song['loudness'])
                    song_meta['speechiness'].append(song['speechiness'])
                    song_meta['tempo'].append(song['tempo'])
                    song_meta['time_signature'].append(song['time_signature'])
                    song_meta['valence'].append(song['valence'])
            sleep(3)        
        except Exception as e:
            print("An error occurred:", str(e))
            sleep(3)
    # Create DataFrame after collecting all data
    return pd.DataFrame.from_dict(song_meta)

# Initialize variables for existing data
existing_data_df = pd.DataFrame()
existing_ids = []

# Try to read the existing data
try:
    existing_data_df = pd.read_excel('song_meta_data.xlsx')
    existing_ids = existing_data_df['id'].tolist()
except FileNotFoundError:
    print("Existing data file not found. Will create a new one.")

# Try to read the new data to be processed
try:
    df = pd.read_excel('top_10_songs.xlsx', sheet_name='Sheet1')
    if 'song_ids' in df.columns:
        song_ids = df['song_ids'].tolist()
    else:
        print("Column 'song_ids' not found in 'top_10_songs.xlsx'.")
        song_ids = []
except FileNotFoundError:
    print("New data file 'top_10_songs.xlsx' not found.")
    song_ids = []

#Filter out song IDs that already exist
new_song_id = [song_id for song_id in song_ids if song_id not in existing_ids]

#Call the function with the filtered list of song IDs
if new_song_id:
    song_meta_df = retrieve_track_data(new_song_id)
    
    #If there's new data, append it to the existing data
    if not song_meta_df.empty:
        all_data_df = pd.concat([existing_data_df, song_meta_df], ignore_index=True)
        all_data_df.to_excel('song_meta_data.xlsx', index=False)
else:
    print("No new songs to add.")