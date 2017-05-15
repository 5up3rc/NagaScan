# NagaScan
NagaScan is a distributed passive scanner for Web application.

# Requirements
## For Web Console:
* sudo pip install mysql-connector
* sudo pip install jinja2
* sudo pip install bleach

## For Scanner:
* sudo apt-get install python-pip python-dev libmysqlclient-dev
* sudo pip install requests
* sudo pip install MySQL-python
* sudo pip install -U selenium
* sudo apt-get install libfontconfig

### For Linux 64-bit:
* wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
* tar -jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2

### For Linux 32-bit:
* wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2
* tar -jxvf phantomjs-2.1.1-linux-i686.tar.bz2

## For Proxy:
* sudo apt-get install python-pip python-dev libmysqlclient-dev
* sudo pip install MySQL-python

### mitmproxy:

#### For Linux (Ubuntu 16):
* sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
* sudo pip3 install mitmproxy

#### For Ubuntu 14.04:
* sudo apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
* sudo pip install "mitmproxy==0.18.2"

#### For macOS:
* brew install python3
* brew install mitmproxy
