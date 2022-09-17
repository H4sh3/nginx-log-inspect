import re

from src.geo import IpCountryResolver

lineformat = re.compile(
    r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)


def parse_message(value):
    data = re.search(lineformat, value)
    if data:
        datadict = data.groupdict()
        datadict["method"] = data.group(6)
        return datadict
    return None


def parse_log_list(log_list):
    for message in log_list:
        value = parse_message(message)
        if value:
            yield value


def add_countries_to_messages(log_list, geolocate, verbose=False):
    ipCountryResolver = IpCountryResolver()

    extended_log_list = []

    len_log_list = len(log_list)
    cnt = 0
    for message in log_list:
        ip = message["ipaddress"]

        if geolocate:
            message["country"] = ipCountryResolver.country_of_ip(ip)
        else:
            message["country"] = ''

        extended_log_list.append(message)

        cnt += 1
        if verbose:
            print(f'{cnt} / {len_log_list}')

    return extended_log_list


def to_ip_log_messages_dict(log_list):
    ip_log_messages_dict = {}

    for m in log_list:
        ip = m["ipaddress"]
        if ip in ip_log_messages_dict:
            ip_log_messages_dict[ip].append(m)
        else:
            ip_log_messages_dict[ip] = [m]

    # sort by number of elements for ip
    ip_log_messages_dict = {k: v for k, v in sorted(
        ip_log_messages_dict.items(), key=lambda item: len(item[1]), reverse=True)}

    return ip_log_messages_dict
