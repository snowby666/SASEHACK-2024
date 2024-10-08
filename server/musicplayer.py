from server.music_artist import *
from server.recommender.api import *
UK = ['GB', 'VG']
US = ['US', 'UM']
EU = ['PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'AN']

def getmusic(artistlist, emotion, genres,  market, pop, type):
    """
    It takes in a list of artists, an emotion, a list of genres, a market, a popularity value, and a
    type value, and returns a list of recommended songs
    
    :param artistlist: a list of artists
    :param emotion: "sad", "energetic", "happy", "depressed"
    :param genres: a list of genres
    :param market: The country code of the market you want to search in
    :param pop: popularity of the song
    :param type: 0 for only songs by the artist, 1 for only songs by other artists, 2 for both
    :return: A list of music IDs
    """
    try:
        recommendmusic = {}
        finallist = []
        for i in artistlist:
            try:
                artist = MusicArtist(f"{i}")
                finallist.append(artist.name)
            except Exception as e:
                pass
        if emotion == "Sad":
            attribute = {
                'target_acousticness':1,
                'target_danceability':0,
                'target_energy':0.3,
                'target_instrumentalness':0.5,
                'target_loudness': -15,
                'target_popularity': pop,
                'target_speechiness':0,
                'target_valence':0
                }
        elif emotion == "Energetic":
            attribute = {
                'target_acousticness':0,
                'target_danceability':0.3,
                'target_energy':1,
                'target_instrumentalness':0,
                'target_loudness': -60,
                'target_popularity': pop,
                'target_speechiness':0.75,
                'target_valence':0.75
                }
        elif emotion == "Happy":
            attribute = {
                'target_acousticness':0.3,
                'target_danceability':0.75,
                'target_energy':0.3,
                'target_instrumentalness':0,
                'target_loudness': -45,
                'target_popularity': pop,
                'target_speechiness':0.5,
                'target_valence':1
                }
        elif emotion == "Depressed":
            attribute = {
                'target_acousticness':0.5,
                'target_danceability':1,
                'target_energy':0,
                'target_instrumentalness':1,
                'target_loudness': 0,
                'target_popularity': pop,
                'target_speechiness':1,
                'target_valence':0.3
                }

        for singer in finallist:
            recommender = Recommender()
            recommender.artists = f"{singer}"
            recommender.genres = genres
            recommender.track_attributes = attribute
            recommender.limit = 100
            recommender.market = f"{market}"
            recommendations = recommender.find_recommendations()
            # print(recommender.artists)
            for recommendation in recommendations['tracks']:
                artistname = recommendation['artists'][0]['name']
                if type == 0:
                    if artistname == singer:
                        # print("%s - %s" % (recommendation['name'], recommendation['artists'][0]['name']))
                        # print(recommendation['external_urls']['spotify'])
                        # print(recommendation['id'])
                        recommendmusic[recommendation['id']] = [recommendation['duration_ms'], artistname.lower(), recommendation['name'].lower()]
                elif type == 1:
                    if artistname != singer:
                        i = recommendation['external_ids']['isrc'][:2]
                        i = i.upper()
                        if i == market or (market == 'UK' and i in UK) or (market == 'EU' and i in EU) or (market == 'US' and i in US):
                            # print("%s - %s" % (recommendation['name'], recommendation['artists'][0]['name']))
                            # print(recommendation['external_urls']['spotify'])
                            # print(recommendation['id'])
                           recommendmusic[recommendation['id']] = [recommendation['duration_ms'], artistname.lower(), recommendation['name'].lower()]
                else:
                    recommendmusic[recommendation['id']] = [recommendation['duration_ms'], artistname.lower(), recommendation['name'].lower()]
        return recommendmusic
    except Exception as e:
        pass