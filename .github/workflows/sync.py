import os

from coze import CozeKnowledge
from utils import pretty_print


def get_actual_urls():
    def path_to_url(path):
        relpath = os.path.relpath(path, os.getcwd())
        repo = os.environ["REPOSITORY_NAME"]
        branch = os.environ["BRANCH_NAME"]
        return f"https://raw.githubusercontent.com/{repo}/{branch}/{relpath}"

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
