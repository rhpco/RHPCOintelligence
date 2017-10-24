'''
Module Certificate Transparency
'''
import bs4
import requests
import texttable as tt

NAME = "Certificate Transparency"
MODULE_NAME = "certificate_transparency"
URL = "https://crt.sh/"
PATH = "?q="
WILDCARD = "%25" # wildcard is % urlencoded


class Result(object):
    _domain=""
    _logged_at = ""
    _not_before = ""
    _issuer_name =""

    def __init__(self,domain,logged_at,not_before,issuer_name):
        self._domain = domain
        self._logged_at = logged_at
        self._not_before = not_before
        self._issuer_name = issuer_name

    def getDomain(self):
        return self._domain
    def getLoggedAt(self):
        return self._logged_at
    def getNotBefore(self):
        return self._not_before
    def getIssuerName(self):
        return self._issuer_name

def help():
    print("%s\tCertificate Transparency Module for domain discovery" % MODULE_NAME)

def execute(target):
    print("%s on %s" % (NAME, target))
    scan(target)

def scan(target):
    # Prepare target replace * with %25
    search_query = target.replace('*', '%25')
    url = '{}{}{}'.format(URL, PATH, search_query)
    r = requests.get(url)
    page = r.content
    soup = bs4.BeautifulSoup(page, 'html.parser')
    trs = soup.findAll('table')[1].find('tr').findAll('tr')
    results = []
    for tr in trs:
        tds = tr.findAll('td')
        if tds:
            single_result = Result(tds[3].string,tds[1].string,tds[2].string,tds[4].findAll('a')[0].string)
            results.append(single_result)
    output(results)
def output(results):
    tab = tt.Texttable()
    headings = ['Domain','Logged At','Not Before','Issuer Name']
    tab.header(headings)
    tab.set_cols_width([50,10,10,50])
    domains = []
    logged_at = []
    not_before = []
    issuer_names = []

    for r in results:
        domains.append(r.getDomain())
        logged_at.append(r.getLoggedAt())
        not_before.append(r.getLoggedAt())
        issuer_names.append(r.getIssuerName())


    for row in zip(domains,logged_at,not_before,issuer_names):
        tab.add_row(row)
    s = tab.draw()
    print (s)
