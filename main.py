import pickle
from database import *


def get_similar_ids(anime_id):
    with open('10recommendation.pickle', 'rb') as file:
        data = pickle.load(file)
    return data[anime_id]


def get_similar_dicts(anime_id):
    sim_animes = get_similar_ids(anime_id)
    anime_dicts = []
    for anime in sim_animes:
        d = get_anime_dict(anime)
        anime_dicts.append(d)
    return anime_dicts


if __name__ == '__main__':
    # Testing
    print(get_similar_dicts(0))
