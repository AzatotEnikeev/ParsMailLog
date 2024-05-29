import datetime
import dataclasses
from typing import Dict, Tuple, Any


@dataclasses.dataclass
class MailLogClassInfo:
    """
         Класс-описание таблицы назначения
         :param дата: Имя таблицы
         :param время: Описание таблицы
         :param id_self: внутренний id
         :param fields: Список полей
         :param src: настройки кластеризации хранения
         """
    date: datetime.date = None
    time: datetime.time = None
    id_self: int = None
    flag: str = None
    mail_adress: str = None
    another_information: str = None


def add_log_info(log_str : str):
    return 0
