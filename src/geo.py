import json
import time
import urllib.request

from os.path import exists


ip_country_dict_path = "ips_to_country_dict.json"


class IpCountryResolver:
    def __init__(self):
        self.GEO_IP_API_URL = 'http://ip-api.com/json/'
        self.load_ip_country_dict()

    def load_ip_country_dict(self):
        if exists(ip_country_dict_path):
            with open(ip_country_dict_path, "r") as f:
                self.ip_country_dict = json.loads(f.read())
        else:
            self.ip_country_dict = {}

    def save_ip_country_dict(self):
        with open(ip_country_dict_path, "w") as f:
            f.write(json.dumps(self.ip_country_dict))

    def country_of_ip(self, ip):
        # check if have resolved this ip already
        if ip in self.ip_country_dict:
            return self.ip_country_dict[ip]

        while(True):
            try:
                req = urllib.request.Request(self.GEO_IP_API_URL+ip)
                response = urllib.request.urlopen(req).read()
                json_response = json.loads(response.decode('utf-8'))
                country = json_response['country']

                # keep track of checked ip's
                self.ip_country_dict[ip] = country
                self.save_ip_country_dict()

                return country
            except:
                print("sleeping")
                time.sleep(61)
