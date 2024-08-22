import json


def pretty_print(jsonable_data, title=None):
    print((f"{title}:\n" if title else "") + json.dumps(jsonable_data, indent=4))
