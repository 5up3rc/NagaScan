# -*- coding: utf-8 -*-

import MySQLdb
import smtplib
import time
from email.mime.text import MIMEText

def highlight(content, color, ENVIRONMENT='Linux'):
    if ENVIRONMENT=='Linux':
        if color == "red":
            content = "\033[1;31;40m{}\033[0m".format(content)
        if color == "green":
            content = "\033[1;32;40m{}\033[0m".format(content)
        if color == "yellow":
            content = "\033[1;33;40m{}\033[0m".format(content)
        if color == "blue":
            content = "\033[1;34;40m{}\033[0m".format(content)
    return content

def escape_content(content):
    content = MySQLdb.escape_string(content)
    return content

def send_mail(to_list,sub,content):
    mail_host="smtp.126.com"
    mail_user="zz790786477"
    mail_pass="Security123!"
    mail_postfix="126.com"

    me="Security Alert"+"<"+mail_user+'@'+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  #gb2312
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def logging(log_file, content):
    f=open(log_file,'a')
    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    f.write(str(now)+': '+content.strip()+'\n')
    f.close
