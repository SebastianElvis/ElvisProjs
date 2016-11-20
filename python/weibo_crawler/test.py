import urllib2

companies = [
    'BABA',
    'JMEI',
    'JD'

    'TCTZF',
    'BIDU',
    'SINA',
    'SOHU',
    'NTES',

    'CHU',
    'CHA',
    'CHL'
]

cookie_str = 'ALF=1482238239; _T_WM=eb005c7d02bf6d595bb3d6c428d22d99; SCF=Au-8Lmr7NmWTYYGK6VBbp3NX61FI963-ucAjAUhPoT-bb1fOWxQsmuzOMGsgB-1WqC0heYZrMJE2cIB85hHyUBU.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh3LNHVkce-0__UlEggblno5JpX5o2p5NHD95QEe050SoBXSK27Ws4Dqcj.i--4iKLsi-24i--4iKLsi-24i--ci-zci-2ci--Ri-zciKnf; SUHB=0oU564H-Aeh0Nm; SSOLoginState=1479646511; SUB=_2A251Ne0QDeTxGeRN61EX9CrJyjyIHXVW2fNYrDV6PUJbkdANLUPikW1XK5ARbEY7u0r08FjiojVzHi-5Cg..; gsid_CTandWM=4upp399e1JDZGUibPwrfs9Fhy8e'
header = {"cookie" : cookie_str,
          'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36'}
url = 'http://weibo.cn/u/2303644510'
req = urllib2.Request(url, headers=header)
r = urllib2.urlopen(req)
print r.read()