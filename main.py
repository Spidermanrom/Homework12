from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def init(self, value):
        self._value = value

    def str(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def init(self, value):
        super().init(value)
        self.validate_phone(value)

    def validate_phone(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Invalid phone number format")


class Birthday(Field):
    def init(self, value):
        super().init(value)
        self.validate_birthday(value)

    def validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format (should be 'YYYY-MM-DD')")


class Record:
    def init(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        initial_length = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone]
        if len(self.phones) == initial_length:
            raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                new_phone_instance = Phone(new_phone)
                if not new_phone_instance.validate_phone(new_phone_instance.value):
                    raise ValueError("Invalid phone number format")
                phone_obj.value = new_phone
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left

    def str(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def init(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, N=1):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]

    def save_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def search(self, query):
        results = []
        for record in self.data.values():
            if query in record.name.value:
                results.append(record)
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
        return results


if __name__ == "__main__":
    address_book = AddressBook()