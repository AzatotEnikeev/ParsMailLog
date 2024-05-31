import datetime
from typing import List

from sqlalchemy import exc, text

from backend.constants import COL_SHOW_TEXT, COL_SHOW_TIME, DATETIME_FORMAT
from backend.mail_log_class import MailLogClassInfo
from sql.database import Session
from sql.models import Log, Message


def add_into_message(
    current_session: Session,
    created: datetime,
    id: str,
    int_id: str,
    str_log: str,
    status: bool,
):
    """
    Добавления записи в таблицу message
    :param current_session: текущая сессия с базой
    :param created: дата + время создания
    :param id: id для сообщения типа ПРИБЫТИЕ
    :param int_id: внутренний id сообщения
    :param str_log: строка лога
    :param status: не описано по заданию, передаю False
    """
    try:
        with current_session.begin():
            current_session.add(
                Message(
                    created=created, id=id, int_id=int_id, str=str_log, status=status
                )
            )  # добавление значений
            current_session.commit()
    except exc.DatabaseError as error:
        print(type(error))
        print(error)


def add_into_log(
    current_session: Session, created: datetime, int_id: str, str_log: str, address: str
):
    """
     Добавления записи в таблицу log
    :param current_session: текущая сессия с базой
    :param created: дата + время создания
    :param int_id: внутренний id сообщения
    :param str_log: строка лога
    :param address: адресс отправителя/получателя
    """
    try:
        with current_session.begin():
            current_session.add(
                Log(created=created, int_id=int_id, str=str_log, address=address)
            )  # добавление значений
            current_session.commit()
    except exc.DatabaseError as error:
        print(type(error))
        print(error)


def format_to_datetime(date_string: str, format=DATETIME_FORMAT) -> datetime:
    return datetime.datetime.strptime(date_string, format)


def set_values_from_mail_log(current_session, list_of_mail_log: List[MailLogClassInfo]):
    """

    :param current_session:
    :param list_of_mail_log:
    :return:
    """
    for value in list_of_mail_log:
        if value.id:
            date_time = format_to_datetime(value.date + " " + value.time)
            add_into_message(
                current_session,
                date_time,
                id=value.id[0],
                int_id=value.id_self,
                str_log=value.another_information,
                status=False,
            )
        else:
            date_time = format_to_datetime(value.date + " " + value.time)
            add_into_log(
                current_session,
                created=date_time,
                int_id=value.id_self,
                str_log=value.another_information,
                address=value.mail_adress,
            )


def select_values_from_tables(current_session: Session, name_address: str) -> List:
    """
    :param current_session: текущая сессия с базой
    :param name_address: имя адреса получателя
    :return:
    """
    name_address = f"'{name_address}'"
    query = text(
        "select created, str, int_id from (select created, str, int_id  from log where log.int_id in"
        " (Select distinct(int_id) from log l where l.address = "
        + name_address
        + ")) t1"
        " union all "
        "select created, str, int_id from (select created, str, int_id from message where  "
        "message.int_id in (Select distinct(int_id) "
        "from log l where l.address ="
        + name_address
        + ") ) t2 order by created, int_id"
    )
    result_from_select = current_session.execute(query).all()
    result_after_format = format_result(result_from_select)
    return result_after_format


def format_result(result: list):
    new_result = []
    for record in result:
        date_to_tsr = record[0]
        new_result.append({COL_SHOW_TIME: str(date_to_tsr), COL_SHOW_TEXT: record[1]})
    return new_result
