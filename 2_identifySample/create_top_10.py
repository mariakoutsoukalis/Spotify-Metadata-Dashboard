import pandas as pd

#Read the Excel file
df = pd.read_excel('spotify_sa_chart.xlsx', sheet_name='Sheet1')

#Group by 'track_name' and aggregate 'streams', 'artist_names', and 'uri'
agg_columns = {
    'streams': 'sum', #values will be summed
    'artist_names': 'first', #assumes first occurrence (all entries for the same track have the same artist name)
    'uri': 'first' # assumes first occurrence (all entries for the same track have the same URI)
}

song_streams = df.groupby('track_name').agg(agg_columns).reset_index() #after aggregate method is complete the track_name column is reset

#Sort by 'streams' in descending order and select the top 10 songs
top_10_songs = song_streams.sort_values(by='streams', ascending=False).head(10)

#Save the top 10 songs to a new Excel file
top_10_songs.to_excel('top_10_songs.xlsx', index=False)

print(top_10_songs)