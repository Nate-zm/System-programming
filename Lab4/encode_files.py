#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import os
import json
import sys
from typing import List, Dict, Optional


def закодировать_файл(файл: str) -> Optional[str]:
    """
    Reads a file in binary mode and returns its Base64-encoded string.
    
    :param файл: Path to the file.
    :return: Base64 string if successful, None otherwise.
    """
    try:
        with open(файл, 'rb') as f:
            binary_data = f.read()
        encoded = base64.b64encode(binary_data).decode('utf-8')
        return encoded
    except FileNotFoundError:
        print(f"[Ошибка] Файл не найден: {файл}", file=sys.stderr)
    except PermissionError:
        print(f"[Ошибка] Нет доступа к файлу: {файл}", file=sys.stderr)
    except Exception as e:
        print(f"[Ошибка] Не удалось закодировать '{файл}': {e}", file=sys.stderr)
    return None


def закодировать_файлы(список_файлов: List[str]) -> Dict[str, str]:
    """
    Encodes multiple files into Base64.
    
    :param список_файлов: List of file paths.
    :return: Dictionary {filename: base64_string}
    """
    результат = {}
    for путь in список_файлов:
        if not os.path.isfile(путь):
            print(f"[Пропущено] Не является файлом: {путь}", file=sys.stderr)
            continue
        имя = os.path.basename(путь)
        данные = закодировать_файл(путь)
        if данные is not None:
            результат[имя] = данные
    return результат


def main():
    # Example: encode all files passed as command-line arguments
    if len(sys.argv) < 2:
        print("Использование: python encode_files.py <file1> [file2] [file3] ...")
        print("Пример: python encode_files.py image.png document.pdf")
        sys.exit(1)

    файлы = sys.argv[1:]
    print(f"Начинаю кодирование {len(файлы)} файл(ов)...")

    закодированные = закодировать_файлы(файлы)

    if not закодированные:
        print("Ни один файл не был успешно закодирован.")
        sys.exit(1)

    # Prepare JSON output (suitable for network transmission)
    try:
        json_output = json.dumps(закодированные, ensure_ascii=False, indent=2)
        # In real network use, you'd send `json.dumps(закодированные)` without indent
        print("\n=== ЗАКОДИРОВАННЫЕ ДАННЫЕ (в формате JSON) ===")
        print(json_output)
    except Exception as e:
        print(f"[Критическая ошибка] Не удалось сериализовать в JSON: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()