import os
import shutil
import datetime
from pathlib import Path

class BackupUtility:
    def __init__(self, source_dir: str, backup_root: str):
        """
        Инициализация утилиты резервного копирования.
        
        :param source_dir: Путь к исходной директории для бэкапа.
        :param backup_root: Корневая директория, где будут храниться бэкапы.
        """
        self.source_dir = Path(source_dir)
        self.backup_root = Path(backup_root)

        if not self.source_path.exists():
            raise ValueError(f"Исходная директория не существует: {self.source_dir}")
        self.backup_root.mkdir(parents=True, exist_ok=True)

    @property
    def source_path(self):
        return self.source_dir

    def _create_backup_folder(self) -> Path:
        """1. Создать папку для бэкапа с текущей датой."""
        today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_folder = self.backup_root / today
        backup_folder.mkdir(exist_ok=True)
        return backup_folder

    def _copy_files_and_structure(self, backup_folder: Path):
        """2 & 3. Скопировать все файлы и структуру поддиректорий."""
        # shutil.copytree копирует всю структуру, но требует, чтобы целевая папка не существовала
        # Поэтому используем обход вручную
        for src_dir, dirs, files in os.walk(self.source_dir):
            # Вычисляем относительный путь от source_dir
            rel_path = Path(src_dir).relative_to(self.source_dir)
            dst_dir = backup_folder / rel_path
            dst_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                src_file = Path(src_dir) / file
                dst_file = dst_dir / file
                shutil.copy2(src_file, dst_file)  # copy2 сохраняет метаданные

    def _count_files(self, path: Path) -> int:
        """Вспомогательный метод для подсчёта файлов в директории (рекурсивно)."""
        return sum(1 for _ in path.rglob('*') if _.is_file())

    def _verify_integrity(self, backup_folder: Path) -> bool:
        """4. Проверить целостность: сравнить количество файлов."""
        source_count = self._count_files(self.source_dir)
        backup_count = self._count_files(backup_folder)
        return source_count == backup_count

    def _cleanup_old_backups(self, days: int = 30):
        """5. Удалить бэкапы старше N дней."""
        now = datetime.datetime.now()
        for item in self.backup_root.iterdir():
            if item.is_dir():
                try:
                    # Имя папки должно быть датой в формате YYYY-MM-DD_HH-MM-SS
                    folder_date = datetime.datetime.strptime(item.name, "%Y-%m-%d_%H-%M-%S")
                    if (now - folder_date).days > days:
                        shutil.rmtree(item)
                        print(f"Удалён старый бэкап: {item}")
                except ValueError:
                    # Игнорируем папки с неподходящим именем
                    continue

    def run_backup(self):
        """Основной метод для запуска резервного копирования."""
        print("Начинаю резервное копирование...")
        backup_folder = self._create_backup_folder()
        print(f"Создана папка бэкапа: {backup_folder}")

        self._copy_files_and_structure(backup_folder)
        print("Файлы и структура скопированы.")

        if self._verify_integrity(backup_folder):
            print("Проверка целостности пройдена успешно.")
        else:
            print("Ошибка: количество файлов не совпадает! Бэкап может быть повреждён.")

        self._cleanup_old_backups(days=30)
        print("Очистка старых бэкапов завершена.")
        print("Резервное копирование завершено.")

# Пример использования:
if __name__ == "__main__":
    source = "C:/Users/Nate/OneDrive/Desktop/System Programming/Lab3"
    backup_root = "C:/Users/Nate/OneDrive/Desktop/System Programming/Backup"

    backup_util = BackupUtility(source, backup_root)
    backup_util.run_backup()