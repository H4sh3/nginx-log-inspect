from pathlib import Path
import src.transform as Transform
import src.extract as Extract
import src.statistics as Statistics
from src.etc import load_data_dict, save_data_dict

# Set this to True to resolve country of each ip
GET_COUNTRIES = True
data_dir = Path('data')


def extract_and_transform(data_dir):

    if GET_COUNTRIES:
        print("Running with ip geo resolve, might take longer!")
    else:
        print("Running...")

    log_list = Extract.get_log_list(data_dir)
    log_list = [v for v in Transform.parse_log_list(log_list)]
    log_list = Transform.add_countries_to_messages(log_list, GET_COUNTRIES, verbose=True)
    ip_log_messages_dict = Transform.to_ip_log_messages_dict(log_list)
    return ip_log_messages_dict


# after running extract_and_transofrm once the data is stored in,
# we can use the preprocessed data from the json file
ip_log_messages_dict = load_data_dict(data_dir)
if ip_log_messages_dict is None:
    ip_log_messages_dict = extract_and_transform(data_dir)
    save_data_dict(data_dir, ip_log_messages_dict)

Statistics.unique_ips(ip_log_messages_dict)

Statistics.common_user_agent(ip_log_messages_dict)

Statistics.common_countries(ip_log_messages_dict)

Statistics.common_status_codes(ip_log_messages_dict)

Statistics.common_ip_adresses(ip_log_messages_dict)

Statistics.common_urls_requested(ip_log_messages_dict, n=10)

Statistics.url_for_status_code(ip_log_messages_dict, 301)

# Statistics.url_requested(ip_log_messages_dict, "robots.txt",shorten_useragents=False)
