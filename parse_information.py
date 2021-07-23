from bs4 import BeautifulSoup


def parse(file_soup):
    # file_soup = open('queue.txt', 'r')    delete this later
    soup = file_soup

    file_list = []

    title = soup.find('div', class_="heading")
    file_list.append(title.text)
    p = soup.find('div', class_="col info")

    for i in range(1, 8):
        value = (p.select(f'p:nth-of-type({i})'))
        soup = BeautifulSoup(str(value[0]), 'lxml')

        list1 = []
        for tag in soup.find_all('a', class_="dotUnder"):
            list1.append(tag.text)

        if i < 5:
            file_list.append(', '.join(list1))
        else:
            stripped = soup.text.strip()
            file_list.append((stripped.split(':')[1]).lstrip())
    str_val = ';'.join(file_list)
    return str_val
