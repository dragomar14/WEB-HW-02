from collections import UserDict
from checking import BirthdayCheck, MailCheck, PhoneCheck
from datetime import datetime
from outputs import AddressbookOutput
import pickle


class PhoneLengthError(Exception):
    """ Exception for wrong length of the phone number """


class PhoneMissing(Exception):
    """ Exception if phone number not found """


class PhoneError(Exception):
    """ Exception when a letter is in the phone number """


class MailTypeError(Exception):
    """ Exception for email mistakes """


class AddressTypeError(Exception):
    """ Exception for address mistakes """


class UserMissing(Exception):
    """ Exception if user not found """


class BirthdayTypeError(Exception):
    """ Exception for birthday format mistakes """


class BirthdayDateError(Exception):
    """ Exception for birthday date mistakes """


class UnknownCommand(Exception):
    """ Exception if user input wrong command """


class AddressExistError(Exception):
    """ Exception if user has an address """


class MailExistError(Exception):
    """Exception if user has an email """


class ElseError(Exception):
    """ Exception for any else errors"""


class AddressBook(UserDict):
    """ Dictionary class """

    def __init__(self):
        super().__init__()
        self.output = AddressbookOutput()

    def read_file(self):
        with open('../../web1hw/AddressBook.bin', 'rb') as reader:
            self.data = pickle.load(reader)
            return self.data

    def write_file(self):
        with open('../../web1hw/AddressBook.bin', 'wb') as writer:
            pickle.dump(self.data, writer)

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def search(self, symb):
        result = []
        for rec in self.data.values():
            if rec in self.data.values():
                if str(symb).lower() in str(rec.name).lower():
                    result.append([rec.name, rec.birthday, rec.mail, rec.address, ", ".join(
                        p.value for p in rec.phones)])
                else:
                    for phone in rec.phones:
                        if str(symb).lower() in str(phone):
                            result.append([rec.name, rec.birthday, rec.mail, rec.address, ", ".join(
                                p.value for p in rec.phones)])
            else:
                continue
        return self.output.create_table(result)

    def show_rec(self, name):
        result = [name, self.data[name].birthday, self.data[name].mail,
                  self.data[name].address, ", ".join(str(p.value) for p in self.data[name].phones)]
        return self.output.create_row(result)

    def show_all_rec(self):
        result = []
        for rec in self.data.values():
            result.append([rec.name, rec.birthday, rec.mail,
                          rec.address, ", ".join([p.value for p in rec.phones])])
        return self.output.create_table(result)

    def change_record(self, name_user, old_record_num, new_record_num):
        record = self.data.get(name_user)
        if record:
            return record.change(old_record_num, new_record_num)
        else:
            raise IndexError("Not enough parameters to execute the command")

    def iterator(self, n=1):
        records = list(self.data.keys())
        records_num = len(records)
        count = 0
        result = []
        if n > records_num:
            n = records_num
        for rec in self.data.values():
            if count < n:
                result.append([rec.name, rec.birthday, rec.mail, rec.address, ", ".join(
                    [p.value for p in rec.phones])])
                count += 1
        yield self.output.create_table(result)


class Field:

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, value):
        self._value = value


class Phone(Field):
    """Class for do phone number standard type"""

    def __init__(self, value):
        super().__init__(value)
        self.phone = PhoneCheck()
        self._value = self.phone.check(value)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, value):
        self._value = self.phone.check(value)


class Birthday(datetime, Field):
    """ Class for creating fields 'birthday' """

    def __init__(self, year, month, day):
        super().__init__()
        self.birth = BirthdayCheck()
        self.__birthday = self.birth.check(year, month, day)

    def __str__(self):
        return str(self.__birthday)

    def __repr__(self):
        return str(self.__birthday)

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.birth.check(year, month, day)


class Mail(Field):
    def __init__(self, value):
        super().__init__(value)
        self.mail = MailCheck()
        self.value = self.mail.check(value)

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.mail.check(value)


class Address(Field):
    def __init__(self, value):
        super().__init__(value)
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, value):
        self._value = value


class Record:
    """ Class for record name or phones"""

    def __init__(self, name, phone=None, birthday=None, mail=None, address=None):
        self.birth = BirthdayCheck()
        if birthday:
            self.birthday = Birthday(*birthday)
        else:
            self.birthday = None
        self.name = name
        self.phone = Phone(phone)
        self.phones = list()
        self.mail = mail
        self.address = address
        if isinstance(phone, Phone):
            self.phones.append(phone)

    def add_phone(self, phone):
        phone = Phone(phone)
        if phone.value:
            lst = [phone.value for phone in self.phones]
            if phone.value not in lst:
                self.phones.append(phone)
                return "Phone was added"
        else:
            raise PhoneError

    def change(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f'{old_phone} to {new_phone} changed'
            else:
                return print(f"Phone {old_phone} not found in the Record")

    def remove_phone(self, phone_num):
        phone = Phone(phone_num)

        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
                return f'Phone {phone_num} deleted'
            else:
                raise PhoneMissing

    def add_user_birthday(self, year, month, day):
        self.birthday = self.birth.check(int(year), int(month), int(day))

    def add_mail(self, mail):
        if not self.mail:
            self.mail = Mail(mail)
        else:
            raise MailExistError

    def del_mail(self):
        self.mail = None

    def chang_mail(self, mail):
        self.mail = Mail(mail)

    def days_to_birthday(self):
        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday is not None:
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            this_year_birthday = datetime(
                cur_year, birthday.month, birthday.day).date()
            delta = this_year_birthday - cur_date
            if delta.days >= 0:
                return f"{self.name}'s birthday will be in {delta.days} days"
            else:
                next_year_birthday = datetime(
                    cur_year + 1, birthday.month, birthday.day).date()
                delta = next_year_birthday - cur_date
                return f"{self.name}'s birthday will be in {delta.days} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def add_address(self, address):
        if not self.address:
            self.address = Address(address)
        else:
            raise AddressExistError

    def change_address(self, address):
        self.address = Address(address)

    def remove_address(self):
        self.address = None


ADDRESSBOOK = AddressBook()