import os
from tqdm import tqdm

def copy_file_with_progress(src: str, dst: str, chunk_size: int = 1024) -> None:
    """
    Копирует файл из src в dst с отображением прогресс-бара.

    :param src: Путь к исходному файлу.
    :param dst: Путь к целевому файлу.
    :param chunk_size: Размер чанка в байтах (по умолчанию 1 КБ).
    :raises FileNotFoundError: Если исходный файл не существует.
    :raises OSError: При ошибках ввода-вывода.
    """
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Исходный файл не найден: {src}")

    file_size = os.path.getsize(src)

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Копирование") as pbar:
            while True:
                chunk = fsrc.read(chunk_size)
                if not chunk:
                    break
                fdst.write(chunk)
                pbar.update(len(chunk))
            
if __name__ == "__main__":
    copy_file_with_progress("test1.txt", "test2.txt")