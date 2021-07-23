from bs4 import BeautifulSoup
import requests
import csv
import parse_information as pi
csv.register_dialect('semicolon-delimited', delimiter=';')


def request_soup(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r, 'lxml')
    return soup


def page_content(URL):
    tables = request_soup(URL).find_all('div', class_="col info")
    for table in tables:
        try:
            # csv_writer.writerow([table.a.text, Base_URL + table.a['href']])
            NEW_URL = Base_URL + table.a['href']

            str_val = (pi.parse(request_soup(NEW_URL)))
            print(f'{NEW_URL} -> {str_val}')
            csv_writer_data.writerow([str_val +';'+ NEW_URL])
        except Exception as e:
            print(e)
            print(f'Error: {NEW_URL}')
            pass


if __name__ == '__main__':

    URL = 'https://readcomiconline.li/Publisher/Archie-Comics'
    comic_name = URL.split('/')[4]
    Base_name = URL.split('/')[2]
    Base_URL = f'https://{Base_name}'

    comic_book_data = open(f"{comic_name}-data.csv", 'w', newline='')
    csv_writer_data = csv.writer(comic_book_data)
    csv_writer_data.writerow(['Name;Genres;Publisher;Writer;Artist;Publication date;Status;Views;URL'])

    while True:
        pages = request_soup(URL).find('a', class_="right_bt next_bt")
        page_content(URL)
        try:
            next_url = pages['href']
            URL = Base_URL + next_url

        except Exception as e:
            print(f'Error: {e}\n End of page reached')
            break
