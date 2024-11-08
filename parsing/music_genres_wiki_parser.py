import requests
from lxml import html


def fetch_genres():
    url = "https://ru.wikipedia.org/wiki/Список_музыкальных_жанров,_направлений_и_стилей"
    response = requests.get(url)

    print(f"Статус ответа: {response.status_code}")  # Отладочный вывод

    if response.status_code != 200:
        print("Не удалось получить данные.")
        return {}

    tree = html.fromstring(response.content)
    genres = {}

    # Находим все основные жанры и их поджанры
    for item in tree.xpath('//div[@id="toc"]//ul//li/a'):
        genre_name = item.text_content().strip()
        genre_link = item.get('href')
        if genre_link and genre_link.startswith('#'):
            # Исключаем "Примечания" и "Литература"
            if genre_name not in ["Примечания", "Литература"]:
                genres[genre_name] = f"https://ru.wikipedia.org{genre_link}"

    print(f"Найдено жанров: {len(genres)}")  # Отладочный вывод
    return genres


def fetch_genre_description(genre_url):
    response = requests.get(genre_url)

    print(f"Статус ответа для {genre_url}: {response.status_code}")  # Отладочный вывод

    if response.status_code != 200:
        print("Не удалось получить данные о жанре.")
        return None

    tree = html.fromstring(response.content)
    description = ""

    # Находим описание жанра
    for paragraph in tree.xpath('//p'):
        description += paragraph.text_content().strip() + "\n"
        if len(description) > 500:  # Ограничиваем длину описания
            break

    return description.strip()


def main():
    genres = fetch_genres()
    if not genres:
        print("Жанры не найдены.")  # Отладочный вывод
        return

    print("Доступные жанры:")
    for i, genre in enumerate(genres.keys(), start=1):
        print(f"{i}. {genre}")

    choice = input("Выберите номер жанра для получения описания (или 'выход' для завершения): ").strip()

    if choice.lower() == 'выход':
        return

    try:
        choice_index = int(choice) - 1
        genre_name = list(genres.keys())[choice_index]
        genre_url = genres[genre_name]

        print(f"\nВы выбрали жанр: {genre_name}")
        description = fetch_genre_description(genre_url)
        if description:
            print(f"\nОписание жанра:\n{description}")
        else:
            print("Описание не найдено.")
    except (ValueError, IndexError):
        print("Некорректный ввод.")


if __name__ == "__main__":
    main()
