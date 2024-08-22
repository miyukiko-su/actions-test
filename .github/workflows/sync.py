import json
import os
import requests


def pretty_print(jsonable_data, title=None):
    print((f"{title}:\n" if title else "") + json.dumps(jsonable_data, indent=4))


class CozeKnowledge:
    def __init__(self, knowledge_id, api_token):
        self.id = knowledge_id
        self.base_url = "https://api.coze.com/open_api/knowledge/document"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Agw-Js-Conv": "str"
        }

    def get(self):
        data = {"dataset_id": self.id}
        response = self.request("list", data)
        urls_by_id = {doc["document_id"]: doc["web_url"] for doc in response.json()["document_infos"]}
        pretty_print(list(urls_by_id.values()), title="Current knowledge list")

        return urls_by_id

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
        response = self.request("create", data)
        pretty_print(urls, title="Adding new documents to knowledge")

    def remove(self, documents):
        data = {"document_ids": list(documents.keys())}
        response = self.request("delete", data)
        pretty_print(list(documents.values()), title="Removing documents from knowledge")

    def request(self, destination, data):
        return requests.post(f"{self.base_url}/{destination}", headers=self.headers, json=data)


def get_actual_urls():
    def path_to_url(path):
        relpath = os.path.relpath(path, os.getcwd())
        url = f"https://raw.githubusercontent.com/{os.environ["REPOSITORY_NAME"]}/{os.environ["BRANCH_NAME"]}/{relpath}"
        return url

    targets = [os.path.join(root, filename) for root, _, files in os.walk(os.getcwd()) for filename in files]
    md_files = [path_to_url(file) for file in targets if file.casefold().endswith(".md")]
    pretty_print(md_files, title="Currently available markdown files")

    return md_files


def main():
    knowledge = CozeKnowledge(
        knowledge_id=os.environ["COZE_KNOWLEDGE_ID"],
        api_token=os.environ["COZE_API_TOKEN"]
    )

    actual_urls = get_actual_urls()
    registered_urls_by_id = knowledge.get()

    if set(actual_urls) == set(registered_urls_by_id.values()):
        print("Finished without updating anything.")
        return

    urls_to_add = [url for url in actual_urls if url not in registered_urls_by_id.values()]
    if urls_to_add:
        knowledge.add(urls_to_add)
    else:
        print("There are no new files to add to knowledge. Skipping...")

    docs_to_remove = {doc_id: url for doc_id, url in registered_urls_by_id.items() if url not in actual_urls}
    if docs_to_remove:
        knowledge.remove(docs_to_remove)
    else:
        print("There are no obsolete files to remove from knowledge. Skipping...")

    knowledge.get()


if __name__ == "__main__":
    main()
