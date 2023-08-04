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

    def fulltext_search_post(self, query: str) -> list[dict]:
        url = f"{self.base_url}/search"
        data = {'query': query}
        response = requests.post(url, json=data)

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

    # Пример полнотекстового поиска с GET запросом
    query = 'Kiersten'
    results_get = client.fulltext_search_get(query)
    print(results_get)

    # # Пример полнотекстового поиска с POST запросом
    # results_post = client.fulltext_search_post(query)
    # print(results_post)
