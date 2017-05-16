# NagaScan
## What is NagaScan
NagaScan is a distributed passive vulnerability scanner for Web application.

## What NagaScan do
NagaScan currently support some common Web application vulnerabilities, e.g. XSS, SQL Injection, File Inclusion etc

## How NagaScan work
Config a proxy, e.g. Web Browser proxy or mobile Wi-Fi proxy, the traffic (including requests headers, cookies, post data, URLs, etc) will be mirrored and parsed into our central database, then NagaScan will be automatically assigned to distributed scanners to scan the common web application vulnerabilities.

# Design
![NagaScan](http://avfisher.win/wp-content/uploads/2017/03/20170313112539_66270.png)

# Requirements
## Web Console
* sudo pip install mysql-connector
* sudo pip install jinja2
* sudo pip install bleach

## Scanner
* sudo apt-get install python-pip python-dev libmysqlclient-dev
* sudo pip install requests
* sudo pip install MySQL-python
* sudo pip install -U selenium
* sudo apt-get install libfontconfig

## Proxy
* sudo apt-get install python-pip python-dev libmysqlclient-dev
* sudo pip install MySQL-python

# Installation & Configuration

## Database
* Install MySQL and create a db user and password, e.g. `root/toor`
* Create database for NagaScan by using command `source schema.sql`

## Web Console
* Modify `www/config_override.py` with your own DB configuration for Web console
```
configs = {
    'db': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'toor'
    }
}
```
* Run `sudo python www/wsgiapp.py` to start Web console

## Scanner
* Modify `scanner/lib/db_operation.py` with your own DB configuration for Scanner
```
def db_conn():
    try:
        user = "root"
        pwd = "toor"
        hostname = "127.0.0.1"
```
* Install PhantomJs
  * Linux 64-bit:
    * wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
    * tar -jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2
  * Linux 32-bit:
    * wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2
    * tar -jxvf phantomjs-2.1.1-linux-i686.tar.bz2
* Modify `scanner/lib/hack_requests.py` in line 28 as below
```
self.executable_path='[Your Own Phantomjs Binary Path]' # e.g. /home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs
```
* Run below commands to start Scanner
  * `python scanner/scan_fi.py` to scan File Inclusion
  * `python scanner/scan_xss.py` to scan XSS
  * `python scanner/scan_sqli.py` to scan SQL injection

## Proxy & Parser
* Install MitmProxy
  * Ubuntu 16.04 (Preferred):
    * sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
    * sudo pip3 install mitmproxy
  * Ubuntu 14.04:
    * sudo apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
    * sudo pip install "mitmproxy==0.18.2"
  * MacOS:
    * brew install python3
    * brew install mitmproxy
* Run `mitmdump -p 443 -s "proxy/proxy_mitmproxy.py /tmp/logs.txt"` to start Proxy
* Modify `parser/lib/db_operation.py` with your own DB configuration for Parser
```
def db_conn():
    try:
        user = "root"
        pwd = "toor"
        hostname = "127.0.0.1"
```
* Run `python parser/parser_mitmproxy.py /tmp/logs.txt` to start Parser

# Usage

* Access to Web Console with the default username and password (*nagascan@example.com/Naga5c@n*) to config exclusions and add SQLMAP server
![webconsole](https://github.com/brianwrf/NagaScan/blob/master/picture/webconsole.jpeg)
![exclusion_1](https://github.com/brianwrf/NagaScan/blob/master/picture/exclusion_1.jpeg)
![exclusion_2](https://github.com/brianwrf/NagaScan/blob/master/picture/exclusion_2.jpeg)
![sqlmapserver](https://github.com/brianwrf/NagaScan/blob/master/picture/sqlmapserver.jpeg)
* Install MitmProxy certificates for Browser or Mobile per [Instruction](http://docs.mitmproxy.org/en/stable/certinstall.html)
* Add a proxy you created in your Web Browser or Mobile Wi-Fi
* Just browse websites from Browser or use APPs from Mobile whatever you like
