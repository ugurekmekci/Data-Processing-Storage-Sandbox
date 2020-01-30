import pandas as pd
# data processing, CSV file I/O (e.g. p# d.read_csv)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

filename = 'top50.csv'
df = pd.read_csv(filename,encoding='ISO-8859-1')
#data = df.head()
#print(data)

df.rename(columns={'Track.Name':'track_name',
	'Artist.Name':'artist_name',
    'Beats.Per.Minute':'beats_per_minute',
    'Loudness..dB..':'Loudness(dB)',
    'Valence.':'Valence',
    'Length.':'Length',
    'Acousticness..':'Acousticness',
    'Speechiness.':'Speechiness'},inplace=True)

#pop = df.loc[(df.Genre == 'pop') & (df.Liveness >= 9)]
pop2 = df.groupby(['Genre']).filter(lambda x : x['Valence'].mean())
#.agg({'Loudness(dB)':['mean']})
#print(pop)
print(pop2)


#Calculating the number of songs of each genre
popular_genre=df.groupby('Genre').size()
popular_artists=df.groupby('artist_name').size()
#df['mostpopular'] = popular_genre.transform('sum')
#print (popular_genre)
TrackNames = df['track_name']
#print (TrackNames)
