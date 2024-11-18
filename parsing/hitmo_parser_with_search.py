from typing import Generator, Dict

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Headers
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# URL сайта
BASE_URL = "https://rus.hitmotop.com/"


def search_music(query):
    # Формируем URL для поиска
    encoded_query = quote(query)  # Кодируем строку запроса
    search_url = f"{BASE_URL}search?q={encoded_query}"

    # Отправка get-запроса на сайт
    response = requests.get(search_url, headers=HEADERS)

    # Проверяем, успешен ли запрос
    if response.status_code == 200:
        return search_url, response.text
    else:
        print("Ошибка при выполнении запроса:", response.status_code)
        return None, None


# Получение имени песни
def get_song_name(track_info):
    song_name = track_info.find(class_="track__title")
    return song_name.text.strip() if song_name else None


# Получение исполнителя песни
def get_song_artist(track_info):
    song_artist = track_info.find(class_="track__desc")
    return song_artist.text.strip() if song_artist else None


# Получение длительности песни
def get_song_time(track_info):
    song_time = track_info.find(class_="track__time")
    return song_time.text.strip() if song_time else None


# Получение ссылки на изображение обложки песни
def get_image_url_song(track_info):
    image = track_info.find(class_="track__img")
    image_url = image["style"][len("background-image: url('"):][:-3]
    return image_url.strip() if image_url else None


# Получение прямой ссылки на скачивание трека
def get_download_song_url(track_info):
    tag_a = track_info.find('a', class_='track__download-btn')
    link = tag_a['href']
    return link.strip() if link else None


def search(query: str) -> Generator[None, None, Dict[str, str]]:
    result_url, page_content = search_music(query)
    soup = BeautifulSoup(page_content, "lxml")

    # Получаем информацию о всех песнях
    all_songs = soup.select(".tracks__item")  # Каждая песня на странице имеет класс "tracks__item"

    if not all_songs:
        print("Не удалось найти песни на странице.")
        return

    for track_info in all_songs:
        song_name = get_song_name(track_info)
        song_artist = get_song_artist(track_info)
        song_time = get_song_time(track_info)
        song_img_url = get_image_url_song(track_info)
        download_song_url = get_download_song_url(track_info)

        # Создаем словарь с информацией о песне
        if song_name and song_artist and song_time:
            yield {
                "name": song_name,
                "artist": song_artist,
                "time": song_time,
                "img": song_img_url,
                "dwnld_link": download_song_url
            }
        else:
            print("Не удалось найти информацию о песне.")


if __name__ == "__main__":
    user_query = input("Введите запрос для поиска музыки: ")

    # Выводим список словарей
    for song in search(user_query):
        print(song)
