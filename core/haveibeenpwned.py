#!/usr/bin/python3
import requests
import json
import subprocess
from time import sleep
from random import randint
from tabulate import tabulate
from colorama import Fore, Style

API_KEY = ""
BREACH_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"
PASTE_URL = "https://haveibeenpwned.com/api/v3/pasteaccount/"

headers = {
    "hibp-api-key": API_KEY,
    "User-Agent": "PwnedHunter.v1"
}

def BreachHunter(accounts):
    doc_name = "haveibeenpwned-breached-table.md"
    breached_data = []
    for account in accounts:
        dates = []
        breaches = []
        resp = requests.get(f"{BREACH_URL}{account}?truncateResponse=false", headers=headers)
        if resp.status_code == 200:
            r = resp.json()
            dates = []
            breaches = []
            for data in r:
                dates.append(data["BreachDate"])
                breaches.append(data["Title"])
        if len(breaches) != 0:
            breached_data.append([account,breaches, dates])
            sleep(randint(3,7))
        else:
            sleep(randint(3,7))
            continue

    print (f"{Fore.YELLOW}[ - ] Saving Table To Disk as Markdown{Style.RESET_ALL}")
    with open(doc_name, 'w') as f:
        f.write(tabulate(breached_data, headers=["Breached Account", "Breach Title", "Breach Date"], tablefmt="github"))
        f.write("\r\n\r\n")
        f.write("asdfasdfas")

    print (f"{Fore.YELLOW}[ - ] Converting Markdown Table to Docx{Style.RESET_ALL}")
    cmd = f"exec pandoc -t docx {doc_name} -o {doc_name}.docx"
    subprocess.Popen(cmd, shell=True)

def PasteHunter(accounts):
    doc_name = "haveibeenpwned-pasted-table.md"
    pasted_data = []
    for account in accounts:
        sources = []
        ids = []
        resp = requests.get(f"{PASTE_URL}{account}", headers=headers)
        if resp.status_code == 200:
            r = resp.json()
            for data in r:
                sources.append(data["Source"])
                ids.append(data["Id"])
        if len(sources) != 0:
            pasted_data.append([account, sources, ids])
            sleep(randint(3,7))
        else:
            sleep(randint(3,7))
            continue

    print (f"{Fore.YELLOW}[ - ] Saving Table To Disk as Markdown{Style.RESET_ALL}")
    with open(doc_name, 'w') as f:
        f.write(tabulate(pasted_data, headers=["Pasted Account", "Paste Source", "Paste ID"], tablefmt="github"))
        f.write("\r\n\r\n")
        f.write("asdfasdfas")

    print (f"{Fore.YELLOW}[ - ] Converting Markdown Table to Docx{Style.RESET_ALL}")
    cmd = f"exec pandoc -t docx {doc_name} -o {doc_name}.docx"
    subprocess.Popen(cmd, shell=True)

def PwnHunter(accounts):
    BreachHunter(accounts)
    paste_data = PasteHunter(accounts)
