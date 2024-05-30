from mail_log_class import MailLogClassInfo
import database
import constants
import re

def parse_log_file(file_name: str, order: list):
    data = []
    file = open(file_name, 'r')
    for line in file.readlines():
        details_line = line.split(" ")
        details = [x.rstrip() for x in details_line]
        mail_log = MailLogClassInfo()

        if details[constants.COL_LOG_FLAG] == '<=':
            if re.findall(r'id=\w*',line):
                mail_log.date = details[constants.COL_LOG_DATE]
                mail_log.time = details[constants.COL_LOG_TIME]
                mail_log.flag = details[constants.COL_LOG_FLAG]
                mail_log.id_self = details[constants.COL_LOG_KEY_ID]
                mail_log.mail_adress = details[constants.COL_LOG_ADDRESS]
                mail_log.another_information = " ".join(details[constants.COL_LOG_ANOTHER_INFO:])
                mail_log.id =  re.findall(r'id=(\S+)',line)
            else:
                continue

        elif details[constants.COL_LOG_FLAG] in ['=>', '->', '**', '==']:

            if len(details) >= 4 and details[constants.COL_LOG_ADDRESS] == ":blackhole:":
                mail_log.date = details[constants.COL_LOG_DATE]
                mail_log.time = details[constants.COL_LOG_TIME]
                mail_log.flag = details[constants.COL_LOG_FLAG]
                mail_log.id_self = details[constants.COL_LOG_KEY_ID]
                mail_log.mail_adress = details[constants.COL_LOG_ADDRESS] + details[constants.COL_LOG_ANOTHER_INFO]
                mail_log.another_information = " ".join(details[constants.COL_LOG_END:])
            else:
                mail_log.date = details[constants.COL_LOG_DATE]
                mail_log.time = details[constants.COL_LOG_TIME]
                mail_log.flag = details[constants.COL_LOG_FLAG]
                mail_log.id_self = details[constants.COL_LOG_KEY_ID]
                mail_log.mail_adress = details[constants.COL_LOG_ADDRESS]
                mail_log.another_information = " ".join(details[constants.COL_LOG_ANOTHER_INFO:])
        else:
            mail_log.date = details[constants.COL_LOG_DATE]
            mail_log.time = details[constants.COL_LOG_TIME]
            mail_log.id_self = details[constants.COL_LOG_KEY_ID]
            mail_log.another_information = " ".join(details[constants.COL_LOG_FLAG:])

        data.append(mail_log)
    file.close()
    return data


if __name__ == "__main__":
    result = parse_log_file('out', order = ["date", "time", "id", "flag", "email", "another information"])
    database.set_values_from_mail_log(result)
    test = 'ffff'
