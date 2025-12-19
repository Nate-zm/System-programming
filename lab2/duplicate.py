import os
import hashlib
from collections import defaultdict

def find_duplicates(directory):
    """
    Находит все дубликаты файлов (по содержимому) в указанной директории.

    :param directory: строка, путь к директории
    :return: словарь, где ключ — хеш содержимого файла,
             значение — список путей к файлам с одинаковым содержимым
    """
    hash_to_files = defaultdict(list)

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            # Пропускаем символические ссылки или директории (если они как файлы)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                        hash_to_files[file_hash].append(filepath)
                except (OSError, IOError):
                    # Игнорируем файлы, которые невозможно прочитать
                    continue

    # Оставляем только те записи, где более одного файла (т.е. дубликаты)
    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}

    return duplicates

# Запрос пути у пользователя
target_dir = input("Введите путь к директории для поиска дубликатов: ").strip()

if not os.path.isdir(target_dir):
    print("Ошибка: указанная директория не существует.")
else:
    duplicates = find_duplicates(target_dir)

    if duplicates:
        print("\nНайдены дубликаты:")
        for h, files in duplicates.items():
            print(f"\nХеш: {h}")
            for f in files:
                print(f" - {f}")
    else:
        print("\nДубликатов не найдено.")