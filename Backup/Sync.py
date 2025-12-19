import os
import shutil
from pathlib import Path
from datetime import datetime

class DirectorySynchronizer:
    def __init__(self, source: str, destination: str):
        """
        Инициализация синхронизатора директорий.

        :param source: Путь к исходной директории (источник).
        :param destination: Путь к целевой директории (приёмник).
        """
        self.source = Path(source).resolve()
        self.destination = Path(destination).resolve()
        self.report = []

        if not self.source.exists() or not self.source.is_dir():
            raise ValueError(f"Исходная директория не существует: {self.source}")

        # Создаём целевую директорию, если её нет
        self.destination.mkdir(parents=True, exist_ok=True)

    def _log(self, message: str):
        """Добавляет сообщение в отчёт и выводит его на экран."""
        self.report.append(message)
        print(message)

    def _get_file_info(self, file_path: Path):
        """Возвращает информацию о файле: (mtime, size)."""
        stat = file_path.stat()
        return stat.st_mtime, stat.st_size

    def _sync_directories(self):
        """Основной метод синхронизации."""
        self._log(f"Начало синхронизации: {self.source} -> {self.destination}")
        self._sync_recursive(self.source, self.destination)
        self._log("Синхронизация завершена.")

    def _sync_recursive(self, src: Path, dst: Path):
        """Рекурсивно синхронизирует поддиректории."""
        # Убедимся, что целевая директория существует
        dst.mkdir(parents=True, exist_ok=True)

        # Получаем множества имён файлов и папок в обеих директориях
        src_items = {item.name: item for item in src.iterdir()}
        dst_items = {item.name: item for item in dst.iterdir()}

        # 1. Обработка файлов и поддиректорий, которые есть в источнике
        for name, src_item in src_items.items():
            dst_item = dst / name

            if src_item.is_dir():
                if dst_item.exists() and not dst_item.is_dir():
                    # В приёмнике файл мешает — удаляем
                    dst_item.unlink()
                    self._log(f"Удалён файл {dst_item} (замена на директорию)")

                # Рекурсивный вызов для поддиректории
                self._sync_recursive(src_item, dst_item)
            else:
                # Это файл
                if not dst_item.exists():
                    # Новый файл — копируем
                    shutil.copy2(src_item, dst_item)
                    self._log(f"Скопирован новый файл: {dst_item}")
                else:
                    # Файл существует — проверяем, нужно ли обновить
                    src_mtime, src_size = self._get_file_info(src_item)
                    dst_mtime, dst_size = self._get_file_info(dst_item)

                    # Сравниваем по времени изменения и размеру
                    if src_mtime > dst_mtime or src_size != dst_size:
                        shutil.copy2(src_item, dst_item)
                        self._log(f"Обновлён устаревший файл: {dst_item}")

        # 2. Удаление лишних файлов и папок в приёмнике
        for name, dst_item in dst_items.items():
            if name not in src_items:
                if dst_item.is_dir():
                    shutil.rmtree(dst_item)
                    self._log(f"Удалена лишняя директория: {dst_item}")
                else:
                    dst_item.unlink()
                    self._log(f"Удалён лишний файл: {dst_item}")

    def synchronize(self):
        """Публичный метод для запуска синхронизации."""
        self.report.clear()
        self._sync_directories()

    def get_report(self) -> list:
        """Возвращает список выполненных действий."""
        return self.report

    def save_report_to_file(self, filepath: str = None):
        """Сохраняет отчёт в файл."""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"sync_report_{timestamp}.txt"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.report))
        self._log(f"Отчёт сохранён в файл: {filepath}")


# Пример использования:
if __name__ == "__main__":
    source_dir = "/Users/Nate/OneDrive/Desktop/System Programming/Lab3"
    dest_dir = "/Users/Nate/OneDrive/Desktop/System Programming/Backup"

    sync = DirectorySynchronizer(source_dir, dest_dir)
    sync.synchronize()

    # Опционально: сохранить отчёт
    sync.save_report_to_file()