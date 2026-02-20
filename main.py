from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


def check_year_grammar(year):
    if year > 9 and year < 21:
        return "лет"
    elif year % 10 in (5, 6, 7, 8, 9, 0):
        return "лет"
    elif year % 10 == 1:
        return "год"
    else:
        return "года"


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

# noinspection PyTypeChecker
wine_src = pandas.read_excel(
    'wine.xlsx',
    sheet_name='Лист1',
    usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
    na_values=['N/A', 'NA'],
    keep_default_na=False
)

wines = wine_src.to_dict(orient='records')
wines_catalogue = collections.defaultdict(list)

for wine in wines:
    category = wine['Категория']
    wines_catalogue[category].append(wine)


def main():
    template = env.get_template('template.html')
    time = datetime.datetime.now().year - datetime.datetime(
        year=1920,
        month=1,
        day=1
    ).year

    rendered_page = template.render(
        time=time,
        wines=wines_catalogue
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
