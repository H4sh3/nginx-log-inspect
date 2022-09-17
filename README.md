# nginx-log-inspect
Small python project that parses the access.log.*.gz files and prints some informations about the requesting clients.

# Start

Geolocating the country of an IP is deactivated by default because it takes some time to run.

The script can be run with `python3 script.py` it will print an output like bellow.

# Data structure after transform
```
ip = datadict["ipaddress"]
datetimestring = datadict["dateandtime"]
url = datadict["url"]
bytessent = datadict["bytessent"]
referrer = datadict["refferer"]
useragent = datadict["useragent"]
status = datadict["statuscode"]
method = datadict["method"]
```