# nginx-log-inspect
Small python project that parses the access.log.*.gz files and prints some informations about the requesting clients.

# Start

### Step 1:
Copy nginx access.log* files in the data folder.

### Step 2:
Run the script with `python3 script.py`, depending on the size of the log files this might take some time.

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