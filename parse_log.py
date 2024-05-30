import re

import database
from constants import (
    BLACKHOLE_STR,
    COL_LOG_ADDRESS,
    COL_LOG_ANOTHER_INFO,
    COL_LOG_DATE,
    COL_LOG_END,
    COL_LOG_FLAG,
    COL_LOG_KEY_ID,
    COL_LOG_TIME,
    FLAG_TYPE_DELIVERY_ARRIVAL,
    MIN_COLS_IF_NOT_ARRIVAL,
    NOT_ARRIVAL_ARRAY_OF_FLAG_TYPE,
    LOG_SEPARATOR
)
from mail_log_class import MailLogClassInfo


def parse_log_file(file_name: str):
    log_result = []
    file = open(file_name, "r")
    for line in file.readlines():
        details_line = line.split(LOG_SEPARATOR)  # разделяем строку по сепаратору
        details = [x.rstrip('\n') for x in details_line]  # убираем символ каретки

        if details[COL_LOG_FLAG] == FLAG_TYPE_DELIVERY_ARRIVAL:
            # обработка случая если сообщение - ПРИБЫТИЕ
            mail_log = convert_str_to_mail_log_class_from_delivery(line, details)

        elif details[COL_LOG_FLAG] in NOT_ARRIVAL_ARRAY_OF_FLAG_TYPE:
            # обработка когда есть флаг и он НЕ ПРИБЫТИЕ
            mail_log = convert_str_to_mail_log_class_from_not_delivery(details)

        else:
            # обработка случая когда в строке нет ФЛАГА
            mail_log = convert_str_to_mail_log_class_from_without_flag(details)

        if mail_log is not None: # убираем случаи, когда mail_log не определился (когда нет id и ПРИБЫТИЕ)
            log_result.append(mail_log)

    file.close()
    return log_result


def convert_str_to_mail_log_class_from_delivery(line: str, details: list[str]) -> MailLogClassInfo:
    mail_log = None
    if re.findall(r"id=\w*", line):  # проверяем что в строке лога есть id
        mail_log = MailLogClassInfo()
        mail_log.id = re.findall(r"id=(\S+)", line)
        mail_log.date = details[COL_LOG_DATE]
        mail_log.time = details[COL_LOG_TIME]
        mail_log.flag = details[COL_LOG_FLAG]
        mail_log.id_self = details[COL_LOG_KEY_ID]
        mail_log.mail_adress = details[COL_LOG_ADDRESS]
        mail_log.another_information = " ".join(details[COL_LOG_ANOTHER_INFO:])

    return mail_log


def convert_str_to_mail_log_class_from_not_delivery(details: list[str]) -> MailLogClassInfo:
    mail_log = MailLogClassInfo()
    if (
            len(details) >= MIN_COLS_IF_NOT_ARRIVAL
            and details[COL_LOG_ADDRESS] == BLACKHOLE_STR
    ):
        mail_log.date = details[COL_LOG_DATE]
        mail_log.time = details[COL_LOG_TIME]
        mail_log.flag = details[COL_LOG_FLAG]
        mail_log.id_self = details[COL_LOG_KEY_ID]
        mail_log.mail_adress = (
                details[COL_LOG_ADDRESS] + details[COL_LOG_ANOTHER_INFO]
        )
        mail_log.another_information = " ".join(details[COL_LOG_END:])
    else:
        mail_log.date = details[COL_LOG_DATE]
        mail_log.time = details[COL_LOG_TIME]
        mail_log.flag = details[COL_LOG_FLAG]
        mail_log.id_self = details[COL_LOG_KEY_ID]
        mail_log.mail_adress = details[COL_LOG_ADDRESS]
        mail_log.another_information = " ".join(details[COL_LOG_ANOTHER_INFO:])
    return mail_log


def convert_str_to_mail_log_class_from_without_flag(details: list[str]) -> MailLogClassInfo:
    mail_log = MailLogClassInfo()
    mail_log.date = details[COL_LOG_DATE]
    mail_log.time = details[COL_LOG_TIME]
    mail_log.id_self = details[COL_LOG_KEY_ID]
    mail_log.another_information = " ".join(details[COL_LOG_FLAG:])
    return mail_log


if __name__ == "__main__":
    result = parse_log_file("out")
    print(result)
    # database.set_values_from_mail_log(result)
    test = "ffff"
