import requests
from RapAnalyzer.models import Song
import time




def pull_from_spotify_playlist(offset=0):
    auth_url = 'https://accounts.spotify.com/api/token'
    body_params = {'grant_type': 'client_credentials'}
    client_id = '08878623e9dd43e587a308889bb9ae4b'
    client_secret = '4ecdc09ebd024cac85e8af7e46079fbc'

    auth_response = requests.post(auth_url, data=body_params, auth=(client_id, client_secret)).json()
    # auth_response = auth_response
    # print(r.json())

    # playlist_id = '37i9dQZF1DX0XUsuxWHRQd'  # Rap Caviar's ID
    # playlist_id = '2zcCNH4mL7OjsqnzrRFaJm'  # Sourish's playlist
    playlist_id = '37i9dQZF1DWUVpAXiEPK8P' # power work out
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Authorization': 'Bearer ' + auth_response['access_token']}
    response = requests.get(url, headers=headers, params={'offset': offset}).json()
    # with open('spotify3.json', 'w') as file:
    #     file.write(str(response['items'][0]['track']['artists'][0]['name']))
    counter = offset + 1
    for track in response['items']:
        try:
            song_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            print(f"{counter}: {song_name} - {artist_name}")
            t0 = time.clock()
            song = Song(song_name, artist_name, '')
            t1 = time.clock()
            print(song.title + ': ' + str(t1 - t0))
            # song.analyze()
            counter += 1
        except:
            pass

    # with open('spotify3.json', 'w') as file:
    #     file.write(str(response['items'][0]['track']['name']))
