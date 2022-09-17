import json
from http.client import responses
from os.path import exists

data_file = "ip_log_message_dict.json"


def save_data_dict(DATA_PATH, data):
    with open(DATA_PATH/data_file, "w") as f:
        f.write(json.dumps(data))


def load_data_dict(DATA_PATH):

    filepath = DATA_PATH/data_file

    if not exists(filepath):
        return None

    with open(filepath, "r") as f:
        return json.loads(f.read())


def status_code_to_text(code):
    try:
        return responses[code]
    except:
        return "Unknown status code"
