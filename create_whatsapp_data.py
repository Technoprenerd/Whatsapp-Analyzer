from myimports import *

def create_whatsapp_data(chat_file, name_person_1, name_person_2):
    person1_datastore = list(dict())
    person2_datastore = list(dict())

    pattern = re.compile("[^\w']")

    def strip_line(line):
        stripped_line = pattern.sub(' ', line).strip()
        datetime_str = stripped_line[0:17]
        datetime_obj = datetime.strptime(datetime_str, '%d %m %y %H %M %S')
        return datetime_obj, stripped_line

    with open(chat_file, "rb") as input_file:
        for line in input_file.readlines():
            if name_person_1 in line:
                datetime_obj, stripped_line = strip_line(line)
                message = stripped_line[34:]
                person1_datastore.append(
                    {'Datetime': str(datetime_obj), 'Message': message})
            if name_person_2 in line:
                datetime_obj, stripped_line = strip_line(line)
                message = stripped_line[35:]
                person2_datastore.append(
                    {'Datetime': str(datetime_obj), 'Message': message})

    input_file.close()

    with open(name_person_1+'_datastore.json', 'w') as outfile:
        json.dump(person1_datastore, outfile)

    with open(name_person_2+'_datastore.json', 'w') as outfile:
        json.dump(person2_datastore, outfile)