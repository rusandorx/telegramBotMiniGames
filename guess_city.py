from random import randint, choice, uniform
import requests

from data import db_session
from data.cities import City


def get_random_spot(toponym):
    toponym_lower, toponym_upper = toponym['boundedBy']['Envelope']['lowerCorner'].split(' '), \
                                   toponym['boundedBy']['Envelope']['upperCorner'].split(' ')
    return ','.join(map(str, (uniform(float(toponym_lower[0]), float(toponym_upper[0])),
                              uniform(float(toponym_lower[1]), float(toponym_upper[1])))))


def get_object_size(toponym):
    toponym_lower, toponym_upper = toponym['boundedBy']['Envelope']['lowerCorner'].split(' '), \
                                   toponym['boundedBy']['Envelope']['upperCorner'].split(' ')
    toponym_size = (float(toponym_upper[0]) - float(toponym_lower[0])) / 8, (
            float(toponym_upper[1]) - float(toponym_lower[1])) / 8
    return ",".join(map(str, toponym_size))


def get_city(city):
    toponym_to_find = " ".join(city)

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"].split()
    toponym3 = get_object_size(toponym)
    map_params = {
        "ll": get_random_spot(toponym),
        "spn": toponym3,
        "l": "sat",
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response.content


async def guess_city(update, context):
    db_session.global_init("db/cities.db")
    context.user_data["game"] = ["guess_city"]
    cities = []
    db_sess = db_session.create_session()
    for city in db_sess.query(City).all():
        cities.append(city)
    s = choice(cities)
    context.user_data["game"].append(s.city)
    await context.bot.send_photo(
        update.message.chat_id,
        get_city(s.city),
        caption=f'Население города {s.population}. Пишите название города на английском языке.'
    )
