import json
import os


def pretty_print(jsonable_data, title=None):
    print((f"{title}:" if title else "") + json.dumps(jsonable_data, indent=4))


def get_actual_urls():
    def path_to_url(path):
        relative_path = os.path.relpath(path, os.getcwd())
        owner = os.environ["REPOSITORY_OWNER"]
        repository_name = os.environ["REPOSITORY_NAME"]
        branch = os.environ["BRANCH_NAME"]

        print(f"relative_path: {relative_path}")
        print(f"owner: {owner}")
        print(f"repository_name: {repository_name}")
        print(f"branch: {branch}")
        
        return f"https://raw.githubusercontent.com/{owner}/{repository_name}/{branch}/{relative_path}"

    target_files = [os.path.join(root, filename) for root, _, files in os.walk(os.getcwd()) for filename in files]
    md_files = [path_to_url(filename) for filename in target_files if filename.casefold().endswith(".md")]
    pretty_print(md_files, title="Currently available markdown files")

    return md_files


get_actual_urls()
  
