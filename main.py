from itertools import chain
from classes import HH, SJ
from utils import *


def get_menu() -> str:
    print("\nВыберите дальнейшее действие:")
    print("1. вывести 5 вакансий с самой высокой оплатой")
    print("2. вывести 5 случайных вакансий")
    print("3. вывести вакансии с зарплатой выше заданной")
    print("4. повторить поиск")
    print("5. выход")
    return input(">>> ")


def change_menu_item(count: int):
    while True:
        user_input = get_menu()  # выбор пункта меню
        vacancies = get_data_of_file()

        if user_input == "1":  # топ 5 зп
            vacancies = get_sort(vacancies)

        elif user_input == "2":  # 5 случайных
            vacancies = get_random(vacancies, count)

        elif user_input == "3":  # зп > указанной
            vacancies = get_more(vacancies, int(input("зп >= ")))

        elif user_input == "4":  # повтор поиска
            break
        elif user_input == "5":  # выход
            exit()
        else:
            print("нет такого пункта")

        rezult = set_rezult_of_file(vacancies)  # запись результата в файл
        for each in rezult:
            print(each, end="")  # вывод результата


def main():
    print("Какие вакансии Вас интересуют?")
    while True:
        keyword = input("введите ключевое слово: ")
        print('идёт поиск подходящих вакансий ...')
        count = 0
        reset_data_of_file()
        for site in (HH(keyword), SJ(keyword)):  # перебор по двум сайтам
            vacancies = site.get_request(1)  # создаём генератор для каждого сайта
            for page in range(2, 50):
                vacancies = chain(vacancies, site.get_request(page))  # добавляем вакансии в генератор

            site_count = set_data_of_file(vacancies)  # запись найденных вакансий в файл
            count += site_count
            print(f" > на сайте {site} найдено {site_count} подходящих вакансий")
        print(f"всего найдено {count} подходящих вакансий")
        change_menu_item(count)  # обработка меню


if __name__ == '__main__':
    main()