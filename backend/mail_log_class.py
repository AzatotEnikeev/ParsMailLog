import dataclasses
import datetime


@dataclasses.dataclass
class MailLogClassInfo:
    """
    Класс-описание таблицы назначения
    :param дата: Имя таблицы
    :param время: Описание таблицы
    :param id_self: внутренний id
    :param fields: Список полей
    :param src: настройки кластеризации хранения
    :param id:  Храним значение идентефикатора id для типа ПРИБЫТИЕ
    """

    date: datetime.date = None
    time: datetime.time = None
    id_self: int = None
    flag: str = None
    mail_adress: str = None
    another_information: str = None
    id: str = None


def add_log_info(log_str: str):
    return 0
