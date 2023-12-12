import pickle
import database as db
import anime_name_recognition as rec


def message(func):
    def in_func(event, *args):
        text = func(event, *args)
        text = text[:1024]
        ans = {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': text,
                'end_session': 'false'
            },
        }
        return ans
    return in_func


@message
def start_message(event):
    size = db.get_database_size()
    return 'Привет! Если вы дадите мне название аниме я подскажу похожие.' + \
           f'\nУ меня в базе целых {size} отличных вариантов!'


@message
def recommendation_message(event, user_anime) -> str:
    anime_id = user_anime['id']
    with open('30rec.pickle', 'rb') as file:
        data = pickle.load(file)
    recs = data[anime_id]
    animes = [db.get_anime_dict(n) for n in recs]
    filtered_animes = rec.remove_seasons(user_anime, animes)
    top3 = filtered_animes[:3]

    def anime_to_text(anime: dict, limit=250):
        text = f'"{anime["name"].strip()}" ({anime["age-rating"]}):\n'
        genres = anime["genres"]
        genres3 = ' '.join(genres.split(', ')[:3])
        text += f'{genres3}\n'
        text += anime["description"]
        return text[:limit-4] + '...\n,\n'

    answer = f'Нашла что-то похожее на "{user_anime["name"].strip()}":\n'
    variants = [
        '',
        'Второй вариант:\n',
        'Третий вариант:\n'
    ]
    for i in range(3):
        answer += variants[i]
        answer += anime_to_text(top3[i])

    answer += 'Также стоит взглянуть на:\n'
    k = 3
    while True:
        added_anime = filtered_animes[k]
        name = f'{added_anime["name"]} ({added_anime["age-rating"]})\n'
        if len(answer + name) > 1024:
            break
        k += 1
        answer += name
    return answer


@message
def unsure_anime_message(event, user_anime):
    answer = recommendation_message(event, user_anime)
    text = answer['response']['text']
    text = text.replace('Нашла что-то похожее на ', 'Кажется вы спросили про: ')
    return text


@message
def help_message(event):
    return 'Напишите мне название аниме, а я расскажу о похожих'


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    text = None
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        text = event['request']['original_utterance']

    if text is None:
        answer = start_message(event)
    elif text.lower() in ["помощь", "что ты умеешь?"]:
        answer = help_message(event)
    else:
        anime_ids = rec.NamesIds()
        anime_id, distance = anime_ids.find_id_and_distance(text)
        user_anime = db.get_anime_dict(anime_id)
        name_len = len(user_anime['name'])
        input_len = len(text)
        best_case_distance = input_len - name_len
        if distance - best_case_distance > name_len * .2:
            answer = unsure_anime_message(event, user_anime)
        else:
            answer = recommendation_message(event, user_anime)

    return answer
