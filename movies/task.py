import abc
import json
from redis import Redis

from typing import Any, Optional

PATH = '/Users/anya/Dev/new_admin_panel_sprint_2/file.json'


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        with open(self.file_path, "w+") as file:
            # data = json.load(file)
            # data.update(state)
            json.dump(state, file)

    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return data


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        try:
            data = self.storage.retrieve_state()
        except:
            return dict()
        else:
            return data.get(key, None)


if __name__ == '__main__':
    storage = JsonFileStorage(PATH)
    stat = State(storage)
    stat.set_state("a", 1)
    print(stat.get_state("a"))