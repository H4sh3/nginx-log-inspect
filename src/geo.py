from codecs import unicode_escape_decode
import json
import time
import urllib.request
from src.etc import chunks

from os.path import exists


ip_country_dict_path = "ips_to_country_dict.json"


class IpCountryResolver:
    def __init__(self):
        self.GEO_IP_API_URL = 'http://ip-api.com/batch'
        self.load_ip_country_dict()
        print(f'Initialized IP-Dict with {len(self.ip_country_dict.keys())} ip\'s')

    def load_ip_country_dict(self):
        if exists(ip_country_dict_path):
            with open(ip_country_dict_path, "r") as f:
                self.ip_country_dict = json.loads(f.read())
        else:
            self.ip_country_dict = {}

    def save_ip_country_dict(self):
        with open(ip_country_dict_path, "w") as f:
            f.write(json.dumps(self.ip_country_dict))

    def resolve_ips(self,unique_ips):
        unknown_ips = [ip for ip in unique_ips if not ip in self.ip_country_dict.keys()]
        ip_chunks =  [i for i in chunks(unknown_ips,100)]
        
        for i,ips in enumerate(ip_chunks):
            print(f"requesting ip countries: {i+1}/{len(ip_chunks)}")
            json_response = self.batch_ips(ips)
            # extend dict with new ip countries
            for entry in json_response:
                self.ip_country_dict[entry["query"]] = entry["country"]


    def batch_ips(self,ips):
        maxtries = 10
        for i in range(maxtries):
            try:
                req = urllib.request.Request(self.GEO_IP_API_URL)
                req.add_header('Content-Type', 'application/json')
                payload = json.dumps(ips).encode('utf-8')
                req.add_header('Content-Length', len(payload))
                response = urllib.request.urlopen(req,payload)
                data = response.read()
                return json.loads(data.decode('utf-8'))

            except Exception as e:
                print(f'{e}! Waiting for 61s and trying again: {i+1}/{maxtries}')
                time.sleep(61)
        
        print(f'Something is wrong with the api... run into multiple request limits')


    def country_of_ip(self, ip):
        # check if have resolved this ip already
        if ip in self.ip_country_dict:
            return self.ip_country_dict[ip]
        else:
            raise("Some ip -> country was not resolved!")

