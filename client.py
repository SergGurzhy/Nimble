import json
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
            return json.loads(data)
        else:
            print(f"Error: {response.status_code}")
            return []

    def get_all(self) -> list[dict]:
        url = f"{self.base_url}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return json.loads(data)
        else:
            print(f"Error: {response.status_code}")
            return []

    def update_info(self) -> None:
        url = f"{self.base_url}/update"
        response = requests.post(url)
        print(response)

    def drop_db(self) -> None:
        url = f"{self.base_url}/drop"
        response = requests.post(url)
        print(response)


if __name__ == '__main__':

    base_url = 'http://127.0.0.1:5000/api'
    client = NimbleDbClient(base_url)

    # Full text search example with GET request
    # query = 'Ferrara'
    # results_get = client.fulltext_search_get(query)
    # pprint.pprint(results_get)

    # client.update_info()

    result_all = client.get_all()
    pprint.pprint(result_all)

    # client.drop_db()
