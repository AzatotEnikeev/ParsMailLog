import json
import maillogclass

def parse_log_file(file_name: str, order: list):
    data = []
    file = open(file_name, 'r')
    for line in file.readlines():
        details = line.split(" ")
        details = [x.rstrip() for x in details]
        new_record = maillogclass.MailLogClassInfo()

        if details[3] in ['<=', '=>', '->', '**', '==']:

            if len(details) > 4 and details[4] == ":blackhole:":
                new_record.date = details[0]
                new_record.time = details[1]
                new_record.flag = details[2]
                new_record.id_self = details[3]
                new_record.mail_adress = details[4] + details[5]
                new_record.another_information = details[6:-1]
            else:
                new_record.date = details[0]
                new_record.time = details[1]
                new_record.flag = details[2]
                new_record.id_self = details[3]
                new_record.mail_adress = details[4]
                new_record.another_information = details[5:-1]
        else:
            new_record.date = details[0]
            new_record.time = details[1]
            new_record.id_self = details[3]
            new_record.another_information = details[4:-1]

        data.append(new_record)
    file.close()
    return data


if __name__ == "__main__":
    result = parse_log_file('out', order = ["date", "time", "id", "flag", "email", "another information"])
    test = 'ffff'
