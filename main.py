"""csv,BeautifulSoup,requests,parse_information.py module."""
import csv
from bs4 import BeautifulSoup
import requests
import parse_information as pi

csv.register_dialect('semicolon-delimited', delimiter=';')


def request_soup(url_holder):
    """ Request HTML source from the page."""
    response = requests.get(url_holder).text
    soup = BeautifulSoup(response, 'lxml')
    return soup


def page_content(url_holder, base_url_holder, comic_name_holder):
    """ Calls the parse_information.py parse()
        function to extract data from each links found on the page."""
    tables = request_soup(url_holder).find_all('div', class_="col info")
    for table in tables:
        new_url = base_url_holder + table.a['href']
        try:
            # csv_writer.writerow([table.a.text, Base_URL + table.a['href']])
            str_val = (pi.parse(request_soup(new_url)))
            print(f'{new_url} -> {str_val}')
            with open(f"{comic_name_holder}-data.csv", 'w', newline='') as comic_book_data:
                csv_writer_data = csv.writer(comic_book_data)
                csv_writer_data.writerow([
                    '''
                    Name;Genres;Publisher;Writer;
                    Artist;Publication date;Status;Views;url_link
                    '''
                ])
                csv_writer_data.writerow([str_val + ';' + new_url])
        except RuntimeError as error:
            print(error)
            print(f'Error: {new_url}')


def main():
    """ Main function."""
    url_link = 'https://readcomiconline.li/Publisher/Archie-Comics'
    comic_name = url_link.split('/')[4]
    base_name = url_link.split('/')[2]
    base_url = f'https://{base_name}'
    with open(f"{comic_name}-data.csv", 'w', newline='') as comic_book_data:
        csv_writer_data = csv.writer(comic_book_data)
        csv_writer_data.writerow([
            '''
                Name;Genres;Publisher;Writer;
                Artist;Publication date;Status;Views;url_link
                '''
        ])

    while True:
        pages = request_soup(url_link).find('a', class_="right_bt next_bt")
        page_content(url_link, base_url, comic_name)
        try:
            next_url = pages['href']
            url_link = base_url + next_url

        except RuntimeError as error:
            print(f'Error: {error}\n End of page reached')
            break
    comic_book_data.close()


if __name__ == '__main__':
    main()
