import datetime
from sqlalchemy import (
    text,
)
from sqlalchemy.orm import session
from sql.models import Message, Log
from backend.mail_log_class import MailLogClassInfo


def add_into_message(created: datetime, id: str, int_id: str, str_log: str, status: bool):
    session.add(
        Message(created=created, id=id, int_id=int_id, str=str_log, status=status)
    )  # поиск и обновление значений
    session.commit()


def add_into_log(created: datetime, int_id: str, str_log: str, address: str):
    session.add(
        Log(created=created, int_id=int_id, str=str_log, address=address)
    )  # поиск и обновление значений
    session.commit()

def format_to_datetime(date_string, format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(date_string, format)


def set_values_from_mail_log(list_of_mail_log: [MailLogClassInfo]):

    for value in list_of_mail_log:
        if value.id:
            date_string = format_to_datetime(value.date + " " + value.time)
            add_into_message(
                date_string,
                id=value.id[0],
                int_id=value.id_self,
                str_log=value.another_information,
                status=False,
            )
        else:
            date_string = format_to_datetime(value.date + " " + value.time)
            add_into_log(
                created=date_string,
                int_id=value.id_self,
                str_log=value.another_information,
                address=value.mail_adress,
            )


def select_values_from_tables(name_address: str):
    name_address = f"'{name_address}'"
    query = text(
        "select * from (select created, str  from log where log.int_id in"
        " (Select distinct(int_id) from log l where l.address = "
        + name_address
        + ")) t1"
        " union all "
        "select * from (select created, str from message where  message.int_id in (Select distinct(int_id) "
        "from log l where l.address =" + name_address + ") ) t2"
    )
    return session.execute(query)


if __name__ == "__main__":
    result = select_values_from_tables("kuxanwyqalsszn@gmail.com")
    for record in result:
        print("\n", record)