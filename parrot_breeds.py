import json

import requests
from bs4 import BeautifulSoup

PARROT_BREEDS_URL = 'https://www.omlet.co.uk/breeds/parrots/'


class HttpError(Exception):
    ...


def get_breeds(raw_data: str) -> list[str]:
    soup = BeautifulSoup(raw_data, 'html.parser')
    raw_breeds = soup.find_all('h6')
    return [breed.text for breed in raw_breeds]


def get_html_page(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise HttpError(f'url={PARROT_BREEDS_URL} status_code={response.status_code}')


def write_in_json(filename: str, data: list) -> None:
    data = {i: val for i, val in enumerate(data)}
    with open(f'{filename}.json', 'w') as f:
        f.write(json.dumps(data, indent=3))


def main():
    raw_data = get_html_page(PARROT_BREEDS_URL)
    breeds: list[str] = get_breeds(raw_data)
    return write_in_json('breeds_60', data=breeds)


if __name__ == '__main__':
    main()
