from typing import Iterator
from abc import ABC, abstractmethod
import requests


class Engine(ABC):

    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    def __init__(self, keywords: str = '') -> None:
        self.url = 'https://api.hh.ru/vacancies/'
        self.params = {'per_page': '20',
                       'text': keywords,
                       'search_field': 'name',
                       'only_with_salary': 'true',
                       'archived': 'false',
                       }

    def __repr__(self) -> str:
        return "hh.ru"

    def get_request(self, pade: int = 1) -> Iterator:
        self.params.update({'page': str(pade)})
        req_data = requests.get(self.url, params=self.params)
        if req_data.status_code == 200:
            for each in req_data.json()['items']:
                title = each['name']
                link = 'https://hh.ru/vacancy/' + each['id']
                desc = each['snippet']['responsibility']
                if not desc:
                    desc = each['snippet']['requirement']
                    if not desc:
                        desc = ""
                teg = 'highlighttext>'  # лишний тег
                desc = desc.replace('<' + teg, '').replace('</' + teg, '')
                salary = each['salary']['from']
                if not salary:
                    salary = each['salary']['to']
                yield {'salary': int(salary),
                       'title': title,
                       'link': link,
                       'desc': desc,

                       }


class SJ(Engine):
    def __init__(self, keywords: str = '') -> None:
        self.url = 'https://russia.superjob.ru/vacancy/search/'
        self.params = f'?keywords={keywords}&pade='

    def __repr__(self) -> str:
        return "SuperJob.ru"

    def get_request(self, pade: int = 1) -> Iterator:
        if pade < 4:
            req_data = requests.get(self.url + self.params + str(pade))
            if req_data.status_code == 200:
                req_items = req_data.text.split('<div class="f-test-search-result-item">')[1:-1]
                for each in req_items:
                    if '<span class="_115dd">Откликнуться</span>' in each:  # исключаем рекламные блоки
                        # ниже сплит-парсинг
                        spliter_1 = '<span class="_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi">'
                        step_0 = each.split('target="_blank" href=')[1].split(spliter_1)

                        step_1 = step_0[0].split('</a>')
                        step_1 = step_1[0].replace('<span class="_1Ijga">', '').replace('</span>', '').split('>')

                        title = step_1[1]
                        link = step_1[0][1:-1]

                        salary = step_0[1].split('</span>')[0]
                        salary = salary.replace('<!-- -->', '').replace('\xa0', '').replace('<span>', '')
                        salary = salary.replace('от', '').replace('до', '').replace('руб.', '').replace('—', '')

                        spliter_2 = '<span class="_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky">'

                        try:
                            desc = step_0[1].split(spliter_2)[1].split('</span>')[0]
                        except:
                            continue

                        desc = desc.replace('<br/>', ' ').replace('<span class="_1Ijga">', '')
                        if salary != 'По говорённости':
                            yield {'salary': int(salary),
                                   'title': title,
                                   'link': 'https://russia.superjob.ru/vakansii/' + link,
                                   'desc': desc,
                                   }