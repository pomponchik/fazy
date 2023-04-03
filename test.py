from collections import UserString


class MyString(UserString):
    pass


assert MyString('lol kek').split() == ['lol', 'kek']
