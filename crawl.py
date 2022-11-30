import requests
from bs4 import BeautifulSoup
import lxml
import json

# # make a request to certik home page
certik_home = 'https://www.certik.com/'
sess = requests.Session()


# get each item on the leader board
url = 'https://www.certik.com/api/projects-list'
page_num = 1 # TODO
data_per_page = 100 # TODO, can be 30, 50, 100
payload = {
    "sort": {},
    "filter": {},
    "currentPage": page_num,
    "dataPerPage": data_per_page
}

# TODO, u need to obtain your own cookie
cookie = 'next-auth.csrf-token=cfec61dccbab0a857916d908506435e31759207c8c3fa230ef1a369cf8c7f2e4|163ec0d60665f34c7ef77b7bc44c116186eb8c0c3e5c2eb595971d71e1f724b9; next-auth.callback-url=https://www.certik.com; _gcl_au=1.1.879389744.1669196118; __hstc=55193076.971c70ebba4715cfcdea9132237c8397.1669196119227.1669196119227.1669196119227.1; hubspotutk=971c70ebba4715cfcdea9132237c8397; __hssrc=1; drift_aid=7a2d1c98-73e8-4da3-b3ae-a1a4985feca1; driftt_aid=7a2d1c98-73e8-4da3-b3ae-a1a4985feca1; _hjSessionUser_2453311=eyJpZCI6IjEwODk4OWJlLWJjYWEtNWI5MS1iMjQ5LTU3MWE4MGY4NWYxMiIsImNyZWF0ZWQiOjE2NjkxOTYxMTc4MTcsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.2.1272404121.1669196114; _hjAbsoluteSessionInProgress=0; _gat_gtag_UA_143369555_13=1; _ga_MY83VE1Y5L=GS1.1.1669347881.3.1.1669347917.24.0.0; _dd_s=logs=1&id=82c3576a-a0a6-4753-907d-71347e9fafaa&created=1669342701285&expire=1669348854085'
# cookie is needed by the api that fetches leader board
sess.headers.update({'cookie': cookie})


resp = sess.post(url=url, data=json.dumps(payload))
data = resp.json()
postfix = []
id = 1
if resp.status_code != 200:
    print("Failed to fetch the leader board, exited.")

for id in range(0, 99):
    postfix.append(data['results'][id]['id'])

for pf in postfix:
    proj_resp = sess.get(url=f"{certik_home}projects/{pf}")
    if proj_resp.status_code == 200:
        soup = BeautifulSoup(proj_resp.content, 'lxml')
        # get the script with specified id
        script = soup.find(
            'script', {'id': '__NEXT_DATA__'}
        )
        for a in json.loads(script.text)['props']['pageProps']['project']['audits']:
            print("report link:", a['reportLink'])
            if a['reportLink'] != None and a['reportLink'] != '' and a['reportLink'] != 'None':
                resp_pdf = sess.get(url=a['reportLink'])
                # save the response content as pdf
                with open(f"{pf}.pdf", 'wb') as f:
                    f.write(resp_pdf.content)
                print(f"saved {pf}.pdf downloaded from {a['reportLink']}")