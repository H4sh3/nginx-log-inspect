import gzip
from os import walk


def get_log_list(DATA_PATH):
    filenames = next(walk(DATA_PATH), (None, None, []))[2]
    filenames = [f for f in filenames if "access.log" in f]

    log_data = []
    for filename in filenames:

        filepath = DATA_PATH / filename

        if '.gz' in filename:
            with gzip.open(filepath) as f:
                data = f.read().decode('utf-8')
                log_data += data.split("\n")
        else:
            with open(filepath, 'r') as f:
                data = f.read()
                log_data += data.split("\n")

    return log_data
