import requests

baseUrl = "http://api.genius.com"

headers = {'Authorization': 'Bearer nkWbkfZE-e1e6ZXD_Iu27Wy141pGCQapbtGOS3mnDJ_R_DNRRgAPRGhSX2LYM2Yn'}
searchUrl = baseUrl + "/search"
songTitle = "Ordinary Man (feat. Elton John)"
artist = 'Ozzy'
data = {'q': 'Ordinary Man (feat. Elton John)'}
response = requests.get(searchUrl, params=data, headers=headers)
json = response.json()
print(json['response'])

for song in json['response']['hits']:
    if artist in song['result']['full_title']:
        print(song['result'])
