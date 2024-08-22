import requests

from utils import pretty_print


class CozeKnowledge:
    def __init__(self, knowledge_id, api_token):
        self.id = knowledge_id
        self.base_url = "https://api.coze.com/open_api/knowledge/document"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Agw-Js-Conv": "str"
        }

    def get(self, compact=True):
        return self.__get_compact() if compact else self.__get_full()

    def __get_compact(self):
        data = {"dataset_id": self.id}
        response = self.__request("list", data)
        urls_by_id = {doc["document_id"]: doc["web_url"] for doc in response.json()["document_infos"]}
        pretty_print(list(urls_by_id.values()), title="Current knowledge list")

        return urls_by_id

    def __get_full(self):
        data = {"dataset_id": self.id}
        response = self.__request("list", data)
        documents = response.json()["document_infos"]
        pretty_print(documents, title="Current knowledge list (with details)")

        return documents

    def add(self, urls):
        data = {
            "dataset_id": self.id,
            "document_bases": [
                {
                    "name": "url",
                    "source_info": {"web_url": url, "document_source": 1},
                    "update_rule": {"update_type": 1, "update_interval": 24 * 7}
                } for url in urls
            ],
            "chunk_strategy": {"chunk_type": 0}
        }
        response = self.__request("create", data)
        pretty_print(urls, title="Adding new documents to knowledge")

    def remove(self, documents):
        data = {"document_ids": list(documents.keys())}
        response = self.__request("delete", data)
        pretty_print(list(documents.values()), title="Removing documents from knowledge")

    def __request(self, destination, data):
        return requests.post(f"{self.base_url}/{destination}", headers=self.headers, json=data)
