import pprint
import requests


class NimbleDbClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fulltext_search_get(self, query: str) -> list[dict]:
        url = f"{self.base_url}/search"
        params = {'query': query}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return []

    def get_all(self) -> list[dict]:
        url = f"{self.base_url}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return []


if __name__ == '__main__':
    # Пример использования клиента
    base_url = 'http://127.0.0.1:5000/api'

    client = NimbleDbClient(base_url)

    # results_get = client.get_all()
    # pprint.pprint(results_get)

    # Full text search example with GET request
    query = 'Gray'
    results_get = client.fulltext_search_get(query)
    pprint.pprint(results_get)

