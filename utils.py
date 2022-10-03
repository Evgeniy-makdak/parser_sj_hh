from typing import Iterator
import json
import random


def reset_data_of_file() -> None:
    """ очищает данные о вакансиях в файле vacances.json"""
    with open("vacances.json", "w", encoding="utf-8") as file:
        file.write("")


def set_data_of_file(data: Iterator) -> int:
    """ записывает данные о вакансиях в файл vacances.json"""
    count = 0
    with open("vacances.json", "a", encoding="utf-8") as file:
        for each in data:
            json.dump(each, file, ensure_ascii=False)
            file.write("\n")
            count += 1
    return count


def set_rezult_of_file(data: Iterator) -> Iterator:
    """ записывает результат в файл rezult.txt"""
    with open("rezult.txt", "w", encoding="utf-8") as file:
        for each in data:
            line = "\n".join([each["title"], str(each["salary"]), each["desc"], each["link"]])
            line = line + "\n" + "-" * 50 + "\n"
            file.write(line)
            yield line


def get_data_of_file() -> Iterator:
    """ считывает данные о вакансиях в файл """
    with open("vacances.json", "r", encoding="utf-8") as file:
        for x in file.readlines():
            yield json.loads(x.strip())


def get_sort(list_lines: Iterator, key: str = "salary") -> Iterator:
    """ сортировка вакансий по полю key (по умолчанию  = размер зп) топ 5 """
    for each in sorted(list_lines, key=lambda x: x[key], reverse=True)[:5]:
        yield each


def get_random(list_lines: Iterator, limit: int) -> Iterator:
    """ выбирает 5 случайных вакансий"""
    list_num = []
    for _ in range(5):
        while True:
            num = random.randint(0, limit - 1)  # получим номер вакансии
            if num not in list_num:
                break
        list_num.append(num)
    num = 0
    for each in list_lines:
        if num in list_num:
            yield each
        num += 1


def get_more(list_lines: Iterator, limit: int) -> Iterator:
    for each in list_lines:
        if int(each["salary"]) >= limit:
            yield each
