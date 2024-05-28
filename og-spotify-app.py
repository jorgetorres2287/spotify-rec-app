import spotipy
import requests
import random
from spotipy.oauth2 import SpotifyClientCredentials
import json

client_id = '0fc9e617fc704e7687f101a0acaf37c2'
client_secret = '37801d4b7ddd42e48007bb446d7e4f24'

auth_manager = SpotifyClientCredentials(client_id='0fc9e617fc704e7687f101a0acaf37c2', client_secret='37801d4b7ddd42e48007bb446d7e4f24')
sp = spotipy.Spotify(auth_manager=auth_manager)

# create dictionary mapping explanation to emotion
emotion_explanations = {
    "joy": "Here's a song that's upbeat and lively, perfect for boosting your mood!",
    "sad": "This song has a melancholic feel, suitable for reflecting on emotions.",
    "calm": "This song has soothing melodies to help you unwind and relax.",
    "energized": "This high-energy track will get you ready to groove!",
    "romantic": "This heartfelt song has a nice romantic feel."
}

# create dictionary mapping quantitative preferences to qualitative preferences
rating_explanations = {
    1: "This indicates a low preference for {}.",
    2: "This suggests a slight preference for {}.",
    3: "This indicates a neutral preference for {}.",
    4: "This suggests a moderate preference for {}.",
    5: "This indicates a strong preference for {}."
}

def main():
    # Replace with your access token
    access_token = get_access_token(client_id, client_secret)

    # headers = {
    #     'Authorization': f'Bearer {access_token}',
    # }

    # response = requests.get('https://api.spotify.com/v1/recommendations/available-genre-seeds', headers=headers)

    # if response.status_code == 200:
    #     genre_seeds = response.json().get('genres', [])
    #     print(json.dumps(genre_seeds, indent=2))
    # else:
    #     print(f'Error: {response.status_code}')
    #     print(response.json())
    
    # define emotions
    emotions = ["joy", "sad", "calm", "energized", "romantic"]

    # get user emotion
    user_emotion = input("How are you feeling right now?\n")
    while user_emotion not in emotions:
        user_emotion = input("Please select from the following options\n[Joy][Energized][Calm][Sad][Romantic]\n")

    # get response on whether they want to edit
    user_edit_response = input("Would you like to specify further? [y/n]\n")
    while user_edit_response not in ['y', 'n']:
        user_edit_response = input("Please input [y] for yes, or [n] for no.")

    # declare variable to pass into parameters function
    user_edited = False
    if user_edit_response == 'y':
        user_edited = True

    # store already viewed tracks
    viewed_tracks_names = []
    while True:
        # get parameters for track filtering
        params = get_params(user_emotion, user_edited)

        # get song recs
        recommendations = get_recommendations(access_token, params)

        # store and shuffle songs to avoid repetition on multiple trials
        tracks = recommendations['tracks']
        random.shuffle(tracks)

        # see if we somehow got no tracks, and rerun it with no edits.
        if len(tracks) == 0:
            print(f"We were unable to find any songs that fit your specifications.\nWe apologize for the inconvenience. Here are some generic [{user_emotion}]-type songs instead.")
            params = get_params(user_emotion, False)
            recommendations = get_recommendations(access_token, params)
            tracks = recommendations['tracks']

        # loop and get the song and artist name
        track_info = []
        for track in tracks:
            track_name = track['name']
            artist_names = ', '.join(artist['name'] for artist in track['artists']) 
            viewed_tracks_names.append(track_name)
            track_info.append(f"{track_name} by {artist_names}")

        # print the qualitative explanation for that specific emotion
        print(emotion_explanations[user_emotion])
        # loop through the info of each track and print
        # check if we ran out of tracks, check if they're satisfied
        for info in track_info:
            print(info)  
            user_edit_response = input("Are you satisfied with this recommendation? [y/n]\n")
            while user_edit_response not in ['y', 'n']:
                user_edit_response = input("Please input [y] for yes, or [n] for no.\n")
            if user_edit_response == 'y':
                print("Thank you for using our service.")
                return  
            elif user_edit_response == 'n' and info == track_info[-1]:
                print("Those are all the available songs! Thank you for using our service.\n")
                return

# use spotify api to request song given parameters
def get_recommendations(access_token, params):
    url = 'https://api.spotify.com/v1/recommendations'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# request an api token from spotify to request songs
def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    token = response.json().get('access_token')
    return token

# get the user quantitative preferences from 1-5
def get_user_input(prompt, feature):
    while True:
        try:
            value = int(input(prompt))
            if value in range(1, 6):
                print(rating_explanations[value].format(feature))
                return value
            else:
                print("Please input a number from 1-5.")
        except ValueError:
            print("Please enter a valid integer from 1 to 5.")

# store and return the specific values that the user inputted
def edit_parameters():
    print("Please rate the following features from 1 to 5:")
    user_energy = get_user_input("On a scale from 1-5, how energetic do you want the song to be?\n", "energy")
    user_tempo = get_user_input("On a scale from 1-5, how high do you want the tempo to be?\n", "tempo")
    user_instrumentalness = get_user_input("On a scale from 1-5, do you prefer a lot of instrumentals?\n", "instrumentalness")
    user_popularity = get_user_input("On a scale from 1-5, how mainstream do you want the song to be?\n", "popularity")

    return user_energy, user_tempo, user_instrumentalness, user_popularity

# adjust the energy with static variables that are unique to each song type
def adjust_energy(user_emotion, user_energy):
    adjust_energy = 0
    if user_energy == 1:
        adjust_energy = -0.2
    elif user_energy == 2:
        adjust_energy = -0.1
    elif user_energy == 3:
        adjust_energy = 0
    elif user_energy == 4:
        adjust_energy = 0.1
    elif user_energy == 5:
       adjust_energy = 0.2

    if user_emotion == "joy":
        min_energy = 0.6 + adjust_energy
        target_energy = 0.8 + adjust_energy
    elif user_emotion == "sad":
        min_energy = 0 + adjust_energy
        target_energy = 0.4 + adjust_energy
    elif user_emotion == "calm":
        min_energy = 0 + adjust_energy
        target_energy = 0.4 + adjust_energy
    elif user_emotion == "energized":
        min_energy = 0.7 + adjust_energy
        target_energy = 0.9 + adjust_energy
    elif user_emotion == "romantic":
        min_energy = 0.2 + adjust_energy
        target_energy = 0.4 + adjust_energy

    #set hard bounds
    if min_energy < 0:
        min_energy = 0
    elif min_energy > 0.9:
        min_energy = 0.9
    if target_energy < 0.1:
        target_energy = 0.1
    elif target_energy > 1.0:
        target_energy = 1.0
    
    return min_energy, target_energy

# adjust the tempo with static variables that are unique to each song type
def adjust_tempo(user_emotion, user_tempo):
    adjust_tempo = 0
    if user_tempo == 1:
        adjust_tempo = -40
    elif user_tempo == 2:
        adjust_tempo = -20
    elif user_tempo == 3:
        adjust_tempo = 0
    elif user_tempo == 4:
        adjust_tempo = 20
    elif user_tempo == 5:
       adjust_tempo = 40

    if user_emotion == "joy":
        min_tempo = 100 + adjust_tempo
        target_tempo = 120 + adjust_tempo
        max_tempo = 140 + adjust_tempo
    elif user_emotion == "sad":
        min_tempo = 20 + adjust_tempo
        target_tempo = 60 + adjust_tempo
        max_tempo = 110 + adjust_tempo
    elif user_emotion == "calm":
        min_tempo = 40 + adjust_tempo
        target_tempo = 60 + adjust_tempo
        max_tempo = 80 + adjust_tempo
    elif user_emotion == "energized":
        min_tempo = 120 + adjust_tempo
        target_tempo = 150 + adjust_tempo
        max_tempo = 180 + adjust_tempo
    elif user_emotion == "romantic":
        min_tempo = 60 + adjust_tempo
        target_tempo = 120 + adjust_tempo
        max_tempo = 140 + adjust_tempo

    #set hard bounds
    if min_tempo < 30:
        min_tempo = 30
    elif min_tempo > 150:
        min_tempo = 150
    if target_tempo < 40:
        target_tempo = 40
    elif target_tempo > 170:
        target_tempo = 170
    if max_tempo < 70:
        max_tempo = 70
    elif max_tempo > 200:
        max_tempo = 200
    
    return min_tempo, target_tempo, max_tempo

# adjust the instrumentalness with static variables that are unique to each song type
def adjust_instrumentalness(user_emotion, user_instrumentalness):
    adjust_instrumentalness = 0
    if user_instrumentalness == 1:
        adjust_instrumentalness = -0.2
    elif user_instrumentalness == 2:
        adjust_instrumentalness = -0.1
    elif user_instrumentalness == 3:
        adjust_instrumentalness = 0
    elif user_instrumentalness == 4:
        adjust_instrumentalness = 0.1
    elif user_instrumentalness == 5:
       adjust_instrumentalness = 0.2

    if user_emotion == "joy":
        min_instrumentalness = 0
        target_instrumentalness = 0.2 + adjust_instrumentalness
    elif user_emotion == "sad":
        min_instrumentalness = 0 + adjust_instrumentalness
        target_instrumentalness = 0.5 + adjust_instrumentalness
    elif user_emotion == "calm":
        min_instrumentalness = 0.2 + adjust_instrumentalness
        target_instrumentalness = 0.5 + adjust_instrumentalness
    elif user_emotion == "energized":
        min_instrumentalness = 0 + adjust_instrumentalness
        target_instrumentalness = 0.1 + adjust_instrumentalness
    elif user_emotion == "romantic":
        min_instrumentalness = 0
        target_instrumentalness = 0.2 + adjust_instrumentalness

    #set hard bounds
    if min_instrumentalness < 0:
        min_instrumentalness = 0
    elif min_instrumentalness > 0.5:
        min_instrumentalness = 0.5
    if target_instrumentalness < 0:
        target_instrumentalness = 0
    elif target_instrumentalness > 0.8:
        target_instrumentalness = 0.8
    
    return min_instrumentalness, target_instrumentalness

# adjust the popularity with static variables that are unique to each song type
def adjust_popularity(user_emotion, user_popularity):
    adjust_popularity = 0
    if user_popularity == 1:
        adjust_popularity = -20
    elif user_popularity == 2:
        adjust_popularity = -10
    elif user_popularity == 3:
        adjust_popularity = 0
    elif user_popularity == 4:
        adjust_popularity = 10
    elif user_popularity == 5:
       adjust_popularity = 20

    if user_emotion == "joy":
        min_popularity = 50 + adjust_popularity
    elif user_emotion == "sad":
        min_popularity = 10 + adjust_popularity
    elif user_emotion == "calm":
        min_popularity = 10
    elif user_emotion == "energized":
        min_popularity = 20 + adjust_popularity
    elif user_emotion == "romantic":
        min_popularity = 30 + adjust_popularity

    #set hard bounds
    if min_popularity < 10:
        min_popularity = 10
    elif min_popularity > 70:
        min_popularity = 70
    
    return min_popularity

# adjust the parameters with static variables that are unique to each song type
def get_params(user_emotion, user_edited):
    user_energy = 0
    user_tempo = 0
    user_instrumentalness = 0
    user_popularity = 0
    if user_edited == True:
        user_energy, user_tempo, user_instrumentalness, user_popularity = edit_parameters()

    # update energy based on user preferences
    min_energy, target_energy = adjust_energy(user_emotion, user_energy)

    # update tempo
    min_tempo, target_tempo, max_tempo = adjust_tempo(user_emotion, user_tempo)

    # update instrumentalness
    min_instrumentalness, target_instrumentalness, = adjust_instrumentalness(user_emotion, user_instrumentalness)

    # update popularity
    min_popularity = adjust_popularity(user_emotion, user_popularity)

    # depending on each emotion, return the paremeters accordingly
    if user_emotion == "joy":
        params = { 
        'limit': '100',  
        'market': 'US',  
        'seed_genres': 'pop,hip-hop,rock,happy,summer', 
        'min_valence': '0.5', 
        'target_valence': '0.8',  
        'min_energy': str(min_energy),  
        'target_energy': str(target_energy),  
        'min_danceability': '0.5', 
        'target_danceability': '0.7',  
        'min_tempo': str(min_tempo),  
        'target_tempo': str(target_tempo), 
        'max_tempo': str(max_tempo),
        'min_popularity': str(min_popularity), 
        'min_acousticness': '0.0',
        'max_acousticness': '0.3',  
        'min_speechiness': '0.0', 
        'max_speechiness': '0.3',  
        'min_instrumentalness': str(min_instrumentalness),  
        'target_intrumentalness': str(target_instrumentalness),
        'max_instrumentalness': '0.5'  
        }  
    elif user_emotion == "sad":
        params = {
        'limit': '100',  
        'market': 'US', 
        'seed_genres': 'sad,blues,romance,',  
        'min_valence': '0.0', 
        'max_valence': '0.8',  
        'target_valence': '0.2',  
        'min_energy': str(min_energy),  
        'max_energy': '0.6', 
        'target_energy': str(target_energy),  
        'min_danceability': '0.0',
        'max_danceability': '0.5',  
        'min_tempo': str(min_tempo), 
        'target_tempo': str(target_tempo),  
        'max_tempo': str(max_tempo),
        'min_popularity': str(min_popularity),  
        'min_instrumentalness': str(min_instrumentalness), 
        'target_intrumentalness': str(target_instrumentalness),
        'max_instrumentalness': 1.0,
    }
    elif user_emotion == "calm":
        params = {
        'limit': '100',  
        'market': 'US', 
        'seed_genres': 'jazz,classical,folk,country,guitar',  
        'max_valence': '0.8', 
        'min_energy': str(min_energy), 
        'target_energy': str(target_energy), 
        'min_tempo': str(min_tempo),  
        'target_tempo': str(target_tempo),  
        'max_tempo': str(max_tempo),
        'min_popularity': str(min_popularity),  
        'min_acousticness': '0.3', 
        'max_acousticness': '1.0',  
        'min_instrumentalness': str(min_instrumentalness),  
        'target_intrumentalness': str(target_instrumentalness),
    }
    elif user_emotion == "energized":
        params = {
        'limit': '100',  
        'market': 'US',
        'seed_genres': 'dance,electronic,house,edm,disco',
        'min_valence': '0.5', 
        'max_valence': '1.0',  
        'target_valence': '0.8', 
        'min_energy': str(min_energy), 
        'max_energy': '1.0',  
        'target_energy': str(target_energy),
        'min_danceability': '0.5', 
        'max_danceability': '1.0',  
        'target_danceability': '0.8',  
        'min_tempo': str(min_tempo),  
        'target_tempo': str(target_tempo),  
        'max_tempo': str(max_tempo),
        'min_popularity': str(min_popularity), 
        'max_acousticness': '0.3',  
        'max_speechiness': '0.5', 
        'min_instrumentalness': str(min_instrumentalness), 
        'target_intrumentalness': str(target_instrumentalness),
        'max_instrumentalness': '0.5', 
    }
    elif user_emotion == "romantic":
        params = {
        'limit': '100', 
        'market': 'US',  
        'seed_genres': 'romantic,ballad,jazz,r&b,soul',  
        'min_valence': '0.4', 
        'max_valence': '0.8', 
        'target_valence': '0.6', 
        'min_energy': str(min_energy),
        'max_energy': '0.6', 
        'target_energy': str(target_energy),  
        'min_danceability': '0.3',  
        'max_danceability': '0.7',  
        'target_danceability': '0.5', 
        'min_tempo': str(min_tempo),  
        'target_tempo': str(target_tempo),  
        'max_tempo': str(max_tempo),
        'min_popularity': str(min_popularity), 
        'min_instrumentalness': str(min_instrumentalness),  
        'target_intrumentalness': str(target_instrumentalness),
        'max_instrumentalness': '0.5',  
    }
    return params


if __name__ == "__main__":
    main()
