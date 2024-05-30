import json
import maillogclass
import database
import const

def parse_log_file(file_name: str, order: list):
    data = []
    file = open(file_name, 'r')
    for line in file.readlines():
        details = line.split(" ")
        details = [x.rstrip() for x in details]
        new_record = maillogclass.MailLogClassInfo()

        if details[const.ROW_LOG_FLAG] in ['<=', '=>', '->', '**', '==']:

            if len(details) >= 4 and details[const.ROW_LOG_ADDRESS] == ":blackhole:":
                new_record.date = details[const.ROW_LOG_DATE]
                new_record.time = details[const.ROW_LOG_TIME]
                new_record.flag = details[const.ROW_LOG_FLAG]
                new_record.id_self = details[const.ROW_LOG_KEY_ID]
                new_record.mail_adress = details[const.ROW_LOG_ADDRESS] + details[const.ROW_LOG_ANOTHER_INFO]
                new_record.another_information = details[const.ROW_LOG_END:]
            else:
                new_record.date = details[const.ROW_LOG_DATE]
                new_record.time = details[const.ROW_LOG_TIME]
                new_record.flag = details[const.ROW_LOG_FLAG]
                new_record.id_self = details[const.ROW_LOG_KEY_ID]
                new_record.mail_adress = details[const.ROW_LOG_ADDRESS]
                new_record.another_information = details[const.ROW_LOG_ANOTHER_INFO:]
        else:
            new_record.date = details[const.ROW_LOG_DATE]
            new_record.time = details[const.ROW_LOG_TIME]
            new_record.id_self = details[const.ROW_LOG_KEY_ID]
            new_record.another_information = details[const.ROW_LOG_FLAG :]

        data.append(new_record)
    file.close()
    return data


if __name__ == "__main__":
    result = parse_log_file('out', order = ["date", "time", "id", "flag", "email", "another information"])
    database.set_values_from_mail_log(result)
    test = 'ffff'
