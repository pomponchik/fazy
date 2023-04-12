# FAZY: lazy f-strings for everyone

[![Downloads](https://pepy.tech/badge/fazy/month)](https://pepy.tech/project/fazy)
[![Downloads](https://pepy.tech/badge/fazy)](https://pepy.tech/project/fazy)
[![codecov](https://codecov.io/gh/pomponchik/fazy/branch/master/graph/badge.svg)](https://codecov.io/gh/pomponchik/fazy)
[![Test-Package](https://github.com/pomponchik/fazy/actions/workflows/coverage.yml/badge.svg)](https://github.com/pomponchik/fazy/actions/workflows/coverage.yml)
[![PyPI version](https://badge.fury.io/py/fazy.svg)](https://badge.fury.io/py/fazy)
[![Supports Python versions 2.7 and 3.5+, including PyPy](https://img.shields.io/pypi/pyversions/fazy.svg)](https://pypi.python.org/pypi/fazy)
[![PyPI version](https://badge.fury.io/py/fazy.svg)](https://badge.fury.io/py/fazy)


Протестировать приоритет локалов над нонлокалами, нонлокалов над глобалами, глобалов над билтинами.

Тест на принт и запись в файл.

Тест с замыканием.

Протестировать извлечение нонлокалов из классов.

Протестировать, что счетчик ссылок на интерполируемый обьект уменьшается после интерполяции.


Что тут должно быть:

1. ограничения

Не работает ин слева
Не работает подсветка синтаксиса
Возможно проблемы с нонлокалами из классов, надо проверить
Отсутствует поддержка встроенного языка форматирования
Нужна осторожность с изменяемыми типами данных
Нужна осторожность с тяжелыми обьектами, на них сохраняются ссылки до первой интерполяции

2. Бенчмарки
С интерполяцией и без, извлечение всех локалов и глобалов тоже отжирает время
Указать оборудование

3. Описание принципа работы
Дать ссылку на другую либу с f-строками

4. Описание использования

Кейс с логгингом, обязательно с готовым примером кода
Кейс с условиями
Кейс с отсутствием фстрок на старых питонах
