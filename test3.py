from musixmatch import Musixmatch

musixmatch = Musixmatch('4d1528d399e3aff9d1dbd6e3943172d9')
response = musixmatch.track_search(q_artist='ozzy', q_track='ordinary', page_size=10, page=1, s_track_rating='desc')

for song in response['message']['body']['track_list']:
    print(song['track']['track_name'])
