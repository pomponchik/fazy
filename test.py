from collections import UserString


class MyString(UserString, str):
    def __init__(self, sec):
        self.sec = sec

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls)

    @property
    def data(self):
        return self.sec


assert MyString('lol kek') not in 'kek'
