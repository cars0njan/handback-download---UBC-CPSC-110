import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import os

# SET VARIABLES HERE
CWL = "you_cwl_here" # ubc cwl username <str>
PWD = "you_password_here" # ubc cwl password <str>
STU_NUM = 00000000 # ubc student number <int>
# FILES ARE DOWNLOAD TO "DOWNLOADS" directory
###

basic = HTTPBasicAuth(CWL, PWD)
root = f"https://cs110.students.cs.ubc.ca/handback/{STU_NUM}/"

def main():
    download(root)
    print('download finished\nsee files in the "DOWNLOADS" folder')

def download(url): #download/ download each sub
    r = requests.get(url, auth=basic)
    if not r.ok:
        print(f"""{url} unreachable.
make sure you set the correct variables 
(CWL, PWD, STU_NUM) in main.py""")
        quit()

    h = r.headers.get('Content-Type')
    soup = BeautifulSoup(r.text, 'html.parser')
    path = f'DOWNLOADS/{url.removeprefix(root).replace('./','').replace(':','_')}'

    if not h or 'html' not in h: #is a file -> download
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(r.content)
    else: #is a webpage -> rec all links
        for i in soup.find_all('a')[5:]:
            link = f'{url}{i.get('href')}'
            download(link)

main()