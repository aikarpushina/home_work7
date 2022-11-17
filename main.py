"""
Создать телефонный справочник с возможностью импорта и экспорта данных в нескольких форматах.
под форматами понимаем структуру файлов, например:в файле на одной строке хранится одна часть записи,
пустая строка - разделитель

    Фамилия_1
    Имя_1
    Телефон_1
    Описание_1

    Фамилия_2
    Имя_2
    Телефон_2
    Описание_2

и т.д.в файле на одной строке хранится все записи, символ разделитель - *;***
Фамилия_1,Имя_1,Телефон_1,Описание_1
Фамилия_2,Имя_2,Телефон_2,Описание_2
"""
from typing import Optional


class Formats:
    ONE_LINE = "one_line"
    MANY_LINES = "many_lines"


SEPARATORS = [",", "*", "#", ";", "***", "###"]


def get_format_file(name: str) -> tuple:
    try:
        with open(file=name, mode="r", encoding="utf-8") as f:
            format = f.readline().replace("format=", "").replace("\n", "")
            separator = f.readline().replace("separator=", "").replace("\n", "")

        if format not in [Formats.ONE_LINE, Formats.MANY_LINES]:
            raise ValueError(f"Формат {format} не поддерживается.")
        if format == Formats.ONE_LINE and separator not in SEPARATORS:
            raise ValueError(f"Разделитель {separator} не поддерживается.")

        return format, separator
    except IOError:
        print("Ошибка чтения файла.")


def read_phonebook(file_name: str, format: str, separator: Optional[str] = None) -> list:
    phonebook = []
    if format == Formats.ONE_LINE:
        with open(file=file_name, mode="r", encoding="utf-8", ) as f:
            for i in range(2):
                f.readline()
            for line in f:
                s_line = line.strip().split(separator)
                phonebook.append(
                    dict(first_name=s_line[0],
                         last_name=s_line[1],
                         phone=s_line[2],
                         description=s_line[3])
                )

    if format == Formats.MANY_LINES:
        with open(file=file_name, mode="r", encoding="utf-8", ) as f:
            for i in range(1):
                f.readline()
            for line in f:
                phonebook.append(
                    dict(first_name=line.strip(),
                         last_name=next(f).strip(),
                         phone=next(f).strip(),
                         description=next(f).strip())
                )
                next(f)

    return phonebook


def save_phonebook(file_name: str, format: str, phonebook: list, separator: Optional[str] = None) -> None:
    if format == Formats.ONE_LINE:
        with open(file=file_name, mode='w', encoding='utf8') as f:
            f.write(f"format={format}\n")
            f.write(f"separator={separator}\n")
            for item in phonebook:
                f.write(f"{item['first_name']}{separator}"
                        f"{item['last_name']}{separator}"
                        f"{item['phone']}{separator}"
                        f"{item['description']}\n")

    if format == Formats.MANY_LINES:
        with open(file=file_name, mode='w', encoding='utf8') as f:
            f.write(f"format={format}\n")
            for item in phonebook:
                f.write(f"{item['first_name']}\n")
                f.write(f"{item['last_name']}\n")
                f.write(f"{item['phone']}\n")
                f.write(f"{item['description']}\n")
                f.write(f"\n")


def search_in_phonebook(
        phonebook: list,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None) -> list:
    result = []
    if first_name:
        result = list(filter(lambda search: search['first_name'] == first_name, phonebook))
    if last_name:
        if not result:
            result = list(filter(lambda search: search['last_name'] == last_name, phonebook))
        else:
            result = list(filter(lambda search: search['last_name'] == last_name, result))
    if phone:
        if not result:
            result = list(filter(lambda search: search['phone'] == phone, phonebook))
        else:
            result = list(filter(lambda search: search['phone'] == phone, result))
    return result


def add_user_in_phonebook(
        phonebook: list,
        phone: str,
        first_name: Optional[str] = "Фамилия",
        last_name: Optional[str] = "Имя",
        description: Optional[str] = "Описание") -> None:
    user = search_in_phonebook(phonebook=phonebook, phone=phone)
    if not user:
        phonebook.append(dict(first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             description=description)
                         )
        print(f"Пользователь успешно добавлен.")
    else:
        print(f"Номер {user[0]['phone']} уже записан у пользователя {user[0]['first_name']} {user[0]['last_name']}")


f_name = "phonebook.txt"
format_file, separator_file = get_format_file(f_name)
phone_book = read_phonebook(file_name=f_name, format=format_file, separator=separator_file)

print(search_in_phonebook(
    phonebook=phone_book,
    first_name="Иванов",
    last_name="Сергей",
    phone="+7(111)000-00-00"))

print(search_in_phonebook(
    phonebook=phone_book,
    first_name="Иванов"))

print(search_in_phonebook(
    phonebook=phone_book,
    last_name="Сергей"))

print(search_in_phonebook(
    phonebook=phone_book,
    phone="+7(777)555-44-33"))

add_user_in_phonebook(phonebook=phone_book, phone="+7(111)000-00-01")
add_user_in_phonebook(phonebook=phone_book, phone="+7(111)000-00-01")

print(search_in_phonebook(
    phonebook=phone_book,
    phone="+7(111)000-00-01"))

add_user_in_phonebook(
    phonebook=phone_book,
    first_name="Тестович",
    last_name="Тест",
    phone="+7(111)000-99-01",
    description="Тут описание",)

add_user_in_phonebook(
    phonebook=phone_book,
    first_name="Тестович",
    last_name="Тест",
    phone="+7(111)000-99-01",
    description="Тут описание",)

save_phonebook(file_name="test_save_many.txt", format=Formats.MANY_LINES, phonebook=phone_book)
save_phonebook(file_name="test_save_one.txt", format=Formats.ONE_LINE, separator="###", phonebook=phone_book)
