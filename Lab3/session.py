import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class SessionManager:
    def __init__(self, sessions_dir: str = None):
        """
        Инициализация менеджера сессий.
        :param sessions_dir: Директория для хранения сессий. По умолчанию — ~/.script_sessions
        """
        if sessions_dir is None:
            self.sessions_dir = Path.home() / ".script_sessions"
        else:
            self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
        self.active_session_file = self.sessions_dir / ".active_session"

    def save_session(self, session_name: str, current_dir: str, command_history: list):
        """
        1. Сохранить состояние сессии в файл.
        :param session_name: Имя сессии.
        :param current_dir: Текущая рабочая директория.
        :param command_history: Список выполненных команд (строки).
        """
        session_path = self.sessions_dir / f"{session_name}.json"
        state = {
            "session_name": session_name,
            "current_directory": str(current_dir),
            "command_history": command_history,
            "saved_at": datetime.now().isoformat()
        }
        with open(session_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4, ensure_ascii=False)
        print(f"Сессия '{session_name}' сохранена.")

    def load_session(self, session_name: str):
        """
        2. Загрузить состояние сессии из файла.
        :return: Словарь с состоянием или None, если сессия не найдена.
        """
        session_path = self.sessions_dir / f"{session_name}.json"
        if not session_path.exists():
            print(f"Сессия '{session_name}' не найдена.")
            return None
        with open(session_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        # Устанавливаем сессию как активную
        with open(self.active_session_file, 'w') as f:
            f.write(session_name)
        print(f"Сессия '{session_name}' загружена и активирована.")
        return state

    def list_sessions(self):
        """
        3. Показать список доступных сессий.
        :return: Список имён сессий.
        """
        session_files = self.sessions_dir.glob("*.json")
        sessions = sorted([f.stem for f in session_files])
        print("Доступные сессии:")
        for s in sessions:
            print(f"  - {s}")
        return sessions

    def delete_session(self, session_name: str):
        """
        4. Удалить сессию по имени.
        """
        session_path = self.sessions_dir / f"{session_name}.json"
        if session_path.exists():
            session_path.unlink()
            # Если удаляемая сессия была активной — снимаем активность
            if self.is_session_active(session_name):
                self._clear_active_session()
            print(f"Сессия '{session_name}' удалена.")
        else:
            print(f"Сессия '{session_name}' не существует.")

    def is_session_active(self, session_name: str = None):
        """
        5. Проверить, активна ли сессия.
        :param session_name: Если указано — проверить конкретную сессию.
                             Если None — вернуть имя активной сессии или None.
        :return: bool (если session_name указан) или str/None (если не указан).
        """
        if not self.active_session_file.exists():
            return None if session_name is None else False

        try:
            with open(self.active_session_file, 'r') as f:
                active = f.read().strip()
        except Exception:
            return None if session_name is None else False

        if session_name is None:
            return active if (self.sessions_dir / f"{active}.json").exists() else None
        else:
            return active == session_name

    def _clear_active_session(self):
        """Внутренний метод: сбросить активную сессию."""
        if self.active_session_file.exists():
            self.active_session_file.unlink()

    def get_active_session_name(self):
        """Удобный метод: получить имя активной сессии (или None)."""
        return self.is_session_active()

# Пример использования:
if __name__ == "__main__":
    sm = SessionManager()

    # Сохраняем сессию
    sm.save_session(
        session_name="my_work",
        current_dir=os.getcwd(),
        command_history=["ls", "cd ..", "python script.py"]
    )

    # Список сессий
    sm.list_sessions()

    # Загружаем
    state = sm.load_session("my_work")
    if state:
        print("Текущая директория:", state["current_directory"])
        print("История:", state["command_history"])

    # Проверка активности
    print("Активная сессия:", sm.get_active_session_name())
    print("Сессия 'my_work' активна?", sm.is_session_active("my_work"))

    # Удаление
    sm.delete_session("my_work")