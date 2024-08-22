import os

from coze import CozeKnowledge


def main():
    CozeKnowledge(
        knowledge_id=os.environ["COZE_KNOWLEDGE_ID"],
        api_token=os.environ["COZE_API_TOKEN"]
    ).get(compact=False)


if __name__ == "__main__":
    main()
