from random import randint
import requests


def get_sity(sity):
    toponym_to_find = " ".join(sity)

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()

    def get_distance(toponym):
        toponym1 = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
        toponym2 = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
        toponym3 = [str(abs(float(toponym1[0]) - float(toponym2[0]))), str(abs(float(toponym1[1]) -
                                                                               float(toponym2[1])))]
        return toponym3

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"].split()
    toponym3 = get_distance(toponym)
    toponym_longitude, toponym_lattitude = toponym_coodrinates
    s = randint(1, 4)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(float(toponym3[0]) / 10 * s), str(float(toponym3[1]) / 10 * s)]),
        "l": "map",
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response.content


async def guess_sity(update, context):
    context.user_data["game"] = ["guess_sity"]
    s = "Москва"
    context.user_data["game"].append(s)
    await context.bot.send_photo(
        update.message.chat_id,
        get_sity(s),
    )
