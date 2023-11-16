import csv
import re
import operator
import itertools


class PhoneBookMaker:
    def __init__(self, input_file_name: str, output_file_name: str):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.contacts_list = self.read_csv_to_list()

    def read_csv_to_list(self) -> list:
        contacts_list = []
        with open(self.input_file_name, encoding="utf8") as f:
            file = csv.reader(f, delimiter=",")
            contacts = list(file)
            keys = contacts[0]
            values = contacts[1:]
            for num, value in enumerate(values):
                contacts_list.append({})
                for key, val in zip(keys, value):
                    contacts_list[num].update({key: val})
            return contacts_list

    def write_list_to_csv(self, dicts):
        keys = list(dicts[0].keys())
        with open(self.output_file_name, "w", encoding="utf8") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(keys)
            for d in dicts:
                datawriter.writerow(d.values())

    @staticmethod
    def fix_phones(text: str) -> str:
        pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
        fixed_phones = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)
        return fixed_phones

    def fix_all_phones(self):
        for raw in self.contacts_list:
            phone_number = raw['phone']
            transformed_phone_number = self.fix_phones(phone_number)
            raw['phone'] = transformed_phone_number

    def fix_names(self):
        for raw in self.contacts_list:
            name_words_list = raw['lastname'].split(' ')
            if len(name_words_list) > 1:
                raw['lastname'] = name_words_list[0]
                raw['firstname'] = name_words_list[1]
                if len(name_words_list) > 2:
                    raw['surname'] = name_words_list[2]
            name_words_list = raw['firstname'].split(' ')
            if len(name_words_list) > 1:
                raw['firstname'] = name_words_list[0]
                raw['surname'] = name_words_list[1]

    def merge_names(self):
        group_list = ['firstname', 'lastname']
        group = operator.itemgetter(*group_list)
        self.contacts_list.sort(key=group)
        grouped = itertools.groupby(self.contacts_list, group)
        merge_data = []
        for (firstname, lastname), groups in grouped:
            merge_data.append({'lastname': lastname, 'firstname': firstname})
            for group in groups:
                data = merge_data[-1]
                for key, value in group.items():
                    if key not in data or [key] == '':
                        data[key] = value
        return merge_data

    def make_right_phone_book(self):
        self.fix_all_phones()
        self.fix_names()
        self.write_list_to_csv(self.merge_names())


if __name__ == '__main__':
    phone_book_maker = PhoneBookMaker(input_file_name="phonebook_raw.csv", output_file_name="phonebook_right.csv")
    phone_book_maker.make_right_phone_book()
