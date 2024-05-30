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
)
from mail_log_class import MailLogClassInfo


def parse_log_file(file_name: str):
    data = []
    file = open(file_name, "r")
    for line in file.readlines():
        details_line = line.split(" ")
        details = [x.rstrip() for x in details_line]
        mail_log = MailLogClassInfo()

        if details[COL_LOG_FLAG] == FLAG_TYPE_DELIVERY_ARRIVAL:
            if re.findall(r"id=\w*", line):
                mail_log.date = details[COL_LOG_DATE]
                mail_log.time = details[COL_LOG_TIME]
                mail_log.flag = details[COL_LOG_FLAG]
                mail_log.id_self = details[COL_LOG_KEY_ID]
                mail_log.mail_adress = details[COL_LOG_ADDRESS]
                mail_log.another_information = " ".join(details[COL_LOG_ANOTHER_INFO:])
                mail_log.id = re.findall(r"id=(\S+)", line)
            else:
                continue

        elif details[COL_LOG_FLAG] in NOT_ARRIVAL_ARRAY_OF_FLAG_TYPE:

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
        else:
            mail_log.date = details[COL_LOG_DATE]
            mail_log.time = details[COL_LOG_TIME]
            mail_log.id_self = details[COL_LOG_KEY_ID]
            mail_log.another_information = " ".join(details[COL_LOG_FLAG:])

        data.append(mail_log)
    file.close()
    return data


if __name__ == "__main__":
    result = parse_log_file("out")
    print(result)
    # database.set_values_from_mail_log(result)
    test = "ffff"
