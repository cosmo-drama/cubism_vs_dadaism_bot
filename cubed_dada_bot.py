import os
from dotenv import load_dotenv
import tweepy
import requests
import json
import random

load_dotenv()

cube_list = []
dada_list = []


def twitter_api():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_cubist_art():
    i = 0
    while i < 53:
        i += 1
        urls = 'https://www.wikiart.org/en/paintings-by-style/cubism?json=2&page=' + str(i)
        r = requests.get(urls)
        parsed = json.loads(r.content)
        cubed_paints = parsed['Paintings']
        cube_list.append(cubed_paints)
        continue
    return cubed_paints


def get_dada_art():
    i = 0
    while i < 7:
        i += 1
        urls = 'https://www.wikiart.org/en/paintings-by-style/dada?json=2&page=' + str(i)
        r = requests.get(urls)
        parsed = json.loads(r.content)
        dada_paints = parsed['Paintings']
        dada_list.append(dada_paints)
        continue
    return dada_paints


def save_json_file(parsed_data):
    painting_list = json.dumps(parsed_data)
    with open('dada_paintings.json', 'w') as f:
        f.write(painting_list)
        f.close()
    print("dada json file has been saved.")


def open_cubed_json_file():
    cubed_paintings = json.load(open('cubed_paintings.json'))
    print("Cubed json file has been opened.")
    return {'cubed_paintings': cubed_paintings}


def open_dada_json_file():
    dada_paintings = json.load(open('dada_paintings.json'))
    print("Dada json file has been opened.")
    return {'dada_paintings': dada_paintings}


def randomly_select_piece(paints_list):
    randomize = random.choice(paints_list)
    random_select = random.choice(randomize)
    print(random_select['title'], random_select['artistName'], random_select['year'], random_select['image'])
    random_image = random_select['image']
    title = random_select['title']
    year = random_select['year']
    artist_name = random_select['artistName']
    return {'random_select': random_select, 'random_image': random_image, 'title': title, 'year': year,
            'artistName': artist_name}


def save_cubed_image(random_image):
    r = requests.get(random_image)
    with open('cubism.jpg', 'wb') as f:
        f.write(r.content)
        print('Image Saved.')
    return r.status_code


def save_dada_image(random_image):
    r = requests.get(random_image)
    with open('dadaism.jpg', 'wb') as f:
        f.write(r.content)
        print('Image Saved.')
    return r.status_code


def assemble_tweet(selected_piece_1, selected_piece_2):
    title_1 = selected_piece_1['title']
    artist_name_1 = selected_piece_1['artistName']
    year_1 = selected_piece_1['year']

    title_2 = selected_piece_2['title']
    artist_name_2 = selected_piece_2['artistName']
    year_2 = selected_piece_2['year']

    print("'" + title_1 + "' " + artist_name_1 + "," + year_1 + "| " + "'"
          + title_2 + "'" + artist_name_2 + "," + year_2)
    tweet = ("'" + title_1 + "' by " + artist_name_1 + " , " + year_1 + ". (cubism).\n\n " + "\t\t\t'"
             + title_2 + "' by " + artist_name_2 + ", " + year_2 + " (dada)." + "\n#cubism #dadaism")

    filenames = ['cubism.jpg', 'dadaism.jpg']
    media_ids = []
    for filename in filenames:
        res = twitter_api().media_upload(filename)
        media_ids.append(res.media_id)

    twitter_api().update_status(status=tweet, media_ids=media_ids)
    print("tweet sent.")


# get_cubist_art()
# get_dada_art()

# save_json_file(dada_list)


# print(selected_cubist_piece['random_image'])

saved_dada = open_dada_json_file()
dada_paintings = saved_dada['dada_paintings']

saved_cubes = open_cubed_json_file()
cubist_paintings = saved_cubes['cubed_paintings']

selected_cubist_piece = randomly_select_piece(cubist_paintings)
selected_dada_piece = randomly_select_piece(dada_paintings)
cubist_image = save_cubed_image(selected_cubist_piece['random_image'])
dadaist_image = save_dada_image(selected_dada_piece['random_image'])

assemble_tweet(selected_cubist_piece, selected_dada_piece)
