import os

def create_file_with_permissions(filepath: str, content: str = "", mode: int = 0o644) -> None:

    # Создаём файл и записываем содержимое
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Устанавливаем права доступа
    os.chmod(filepath, mode)

# Пример 1: Создать файл с правами 644 и текстом
create_file_with_permissions("create_file.txt", "Привет, мир!", 0o644)

# Пример 2: Создать исполняемый скрипт
#create_file_with_permissions("script.sh", "#!/bin/bash\necho 'Hello'", 0o755)