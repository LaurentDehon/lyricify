import requests
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer nkWbkfZE-e1e6ZXD_Iu27Wy141pGCQapbtGOS3mnDJ_R_DNRRgAPRGhSX2LYM2Yn'}

song_title = "ordinary man"
artist_name = "ozzy"


def get_lyrics(api_path):
    song_url = base_url + api_path
    res = requests.get(song_url, headers=headers)
    j = res.json()
    song_path = j["response"]["song"]["path"]
    page_url = "http://genius.com" + song_path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics


if __name__ == "__main__":
    search_url = base_url + "/search"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        print(get_lyrics(song_api_path))
