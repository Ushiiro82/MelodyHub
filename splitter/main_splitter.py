import os
from spleeter.separator import Separator

def separate_audio(file_path, output_dir='output'):
    """
    Загружает MP3 файл и разделяет его на дорожки.

    :param file_path: Путь к загружаемому MP3 файлу.
    :param output_dir: Папка для сохранения разделенных дорожек.
    """
    # Проверяем, существует ли файл
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    # Создаем выходную папку, если она не существует
    os.makedirs(output_dir, exist_ok=True)

    # Разделяем дорожки
    separator = Separator('spleeter:4stems')  # 4 дорожки: вокал, ударные, бас, другие
    separator.separate_to_file(file_path, output_dir)

    print(f"Файл {file_path} успешно разделен. Результаты сохранены в {output_dir}.")

# Пример использования
if __name__ == '__main__':
    try:
        separate_audio('/home/ushiiro/Загрузки/MAYOT_-_Killer_Prod_by_malenkiyyarche_x_kayyo_72877437.mp3')
    except Exception as e:
        print(f"Произошла ошибка: {e}")
