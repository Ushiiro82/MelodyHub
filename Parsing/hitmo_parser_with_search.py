"""Этот код с первой на странице песни
извлекает ее название, исполнителя длительность."""


import requests
from bs4 import BeautifulSoup
from urllib.parse import quote



# Headers
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# URL сайта
def search_music(query):
    # Формируем URL для поиска
    base_url = "https://rus.hitmotop.com/"
    encoded_query = quote(query)  # Кодируем строку запроса
    search_url = f"{base_url}search?q={encoded_query}"

    # Отправка get-запроса на сайт
    response = requests.get(search_url, headers=headers)

    # Создание объекта Beautisulsoup
    soup = BeautifulSoup(response.text, "lxml")

    # Проверяем, успешен ли запрос
    if response.status_code == 200:
        # Возвращаем URL страницы с результатами поиска
        return search_url
    else:
        print("Ошибка при выполнении запроса:", response.status_code)
        return None


# Получение имени песни
def get_song_name(parsed_soup):
    song_name = parsed_soup.select_one(".track__info .track__info-l .track__title")
    return song_name.text.strip() if song_name else None

# Получение исполнителя песни
def get_song_desc(parsed_soup):
    song_desc = parsed_soup.find(class_="track__desc")
    return song_desc.text.strip() if song_desc else None

# Получение длительности песни
def get_song_time(parsed_soup):
    song_time = parsed_soup.find(class_="track__time")
    return song_time.text.strip() if song_time else None


if __name__ == "__main__":
    user_query = input("Введите запрос для поиска музыки: ")
    result_url = search_music(user_query)
    page_content = search_music(user_query)

    if result_url:
        print("URL страницы с результатами поиска:", result_url)

        # Парсим HTML-код страницы с результатами
        soup = BeautifulSoup(page_content, "lxml")

        # Получаем информацию о первой песне
        song_name = get_song_name(soup)
        song_desc = get_song_desc(soup)
        song_time = get_song_time(soup)

        # Выводим информацию о первой песне
        if song_name and song_desc and song_time:
            print("Название песни:", song_name)
            print("Исполнитель:", song_desc)
            print("Время песни:", song_time)
        else:
            print("Не удалось найти информацию о первой песне.")
