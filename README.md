# 458
CS458 Automated Decisions Systems - Final Project

# GETTING STARTED
    CLIENT ID: 0fc9e617fc704e7687f101a0acaf37c2
    CLIENT SECRET: 37801d4b7ddd42e48007bb446d7e4f24

# Project Overview:
The Mood-Based Music Recommendation System is designed to offer personalized song suggestions tailored to the user's current emotional state. Leveraging the Spotify API, this system allows users to input their mood and optionally adjust preferences to receive customized song recommendations. By analyzing the user's mood and preferences, the system aims to enhance the music listening experience by providing relevant and enjoyable song choices.

# Description:
At its core, the system functions by first prompting users to input their current mood. Users can choose from a predefined list of mood categories, including joy, sadness, calmness, being energized, or feeling romantic. Each mood category is accompanied by an explanation to help users make informed selections. Additionally, users have the option to further refine their recommendations by adjusting preferences such as energy, tempo, instrumentalness, and popularity on a scale from 1 to 5.

# Significance:
The significance of this project lies in its ability to offer personalized music recommendations that align with the user's emotional state and preferences. By incorporating user input and dynamically adjusting recommendation parameters, the system aims to provide a tailored music listening experience. This personalized approach enhances user satisfaction and engagement, increasing the likelihood of discovering new and enjoyable music.

# Decision Making:
The decision-making process of the system involves several key steps. Firstly, users select their current mood, which determines the initial set of song recommendations. The system provides explanations for each mood category to guide users in making suitable choices. Users can then adjust preferences to further refine their recommendations, with the system dynamically adjusting parameters based on these preferences. Song recommendations are generated from the Spotify API, which contains thousands of songs and their key features, shuffled, and presented to the user along with explanations for each song's suitability. Users can interact with the system by accepting or rejecting recommendations, with the system providing additional suggestions until a suitable song is found.

# Setup
*Have Python installed on your system. Required Python libraries: spotipy, requests.

*[Only use if you are having issues with the client ID and secret, however the ones we provided should work just fine.]Obtain Spotify API credentials (client ID and client secret) from the ([Spotify Developer Dashboard.](https://developer.spotify.com/documentation/web-api/tutorials/getting-started))

*Install the required Python libraries using pip:
`pip install spotipy requests`

*Run the Python script using the command:
`python final.py`


# Usage:
To use the Mood-Based Music Recommendation System, users need to run the provided Python script after setting up their Spotify API credentials. Upon running the script, users will be prompted to input their current mood and optionally adjust preferences. The system will then generate personalized song recommendations based on the user's input, providing explanations for each recommendation. Users can interact with the system by accepting or rejecting recommendations until they find a suitable song.

