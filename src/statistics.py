from collections import Counter

from src.etc import status_code_to_text

from itertools import islice

def unique_ips(ip_request_dict):
    print('- - - Unique ip\'s - - -')

    country_set = set()
    for ip in ip_request_dict:
        country_set.add(ip_request_dict[ip][0]["country"])

    print(f'Found {len(ip_request_dict.keys())} unique ip adresses from {len(country_set)} countries!')

def common_countries(ip_request_dict):
    c = Counter([ip_request_dict[ip][0]["country"] for ip in ip_request_dict])

    n = 10
    print('\n')
    print(f'- - - Top {n} most common countries - - -')
    for agent in c.most_common(n):
        print(f'Requests: {agent[1]}\t Country: {agent[0]}')


def common_user_agent(ip_request_dict):
    agents = []
    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            agents.append(message["useragent"])

    c = Counter(agents)

    n = 10
    print('\n')
    print(f'- - - Top {n} most common user agents - - -')
    for agent in c.most_common(n):
        print(f'Requests: {agent[1]}\tUseragent: {agent[0]}')


def common_status_codes(ip_request_dict):
    agents = []
    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            agents.append(message["statuscode"])

    c = Counter(agents)

    n = 10
    print('\n')
    print(f'- - - Top {n} most common status codes - - -')
    for agent in c.most_common(n):
        print(
            f'Requests: {agent[1]}\tStatuscode: {agent[0]} ->\t{status_code_to_text(int(agent[0]))}')


def common_ip_adresses(ip_request_dict):
    n = 10
    print('\n')
    print(f'- - - Top {n} most common ip adresses - - -')
    for ip in islice(ip_request_dict, n):
        print(f'Requests: {len(ip_request_dict[ip])}\tIP: {ip}')


def common_urls_requested(ip_request_dict, ip=None,n=10):
    urls = []
    for ip_entry in ip_request_dict.items():
        # log oncly specific ip
        if ip != None and ip_entry[0] != ip:
            continue
        urls += [message["url"] for message in ip_entry[1]]

    c = Counter(urls)
    print('\n')
    print(
        f'- - - Top {n} most common urls requested {"by" if ip != None else ""} {ip if ip != None else ""}- - -')
    for value in c.most_common(n):
        print(f'Requests: {value[1]}\t Url: {value[0]}')


def url_for_status_code(ip_request_dict, status_code):
    urls = []
    for ip_entry in ip_request_dict.items():

        for message in ip_entry[1]:
            if int(message["statuscode"]) != status_code:
                continue

            urls.append(message["url"])

    c = Counter(urls)

    n = 10
    print('\n')
    print(
        f'- - - Top {n} most common urls for status code {status_code} -> {status_code_to_text(status_code)}- - -')
    for value in c.most_common(n):
        print(f'Requests:{value[1]}\tUrl: {value[0]}')


def url_requested(ip_request_dict, url,shorten_useragents):
    print('\n')
    print(
        f'- - - IP\'s that requested the url {url} - - -')

    for ip in ip_request_dict:
        for message in ip_request_dict[ip]:
            if url in message["url"]:
                country = message["country"]
                url = message["url"]
                
                if shorten_useragents:
                    agent = message["useragent"][:25]
                else:
                    agent = message["useragent"]

                print(f'{ip} {country} {url} {agent}...')
                break
