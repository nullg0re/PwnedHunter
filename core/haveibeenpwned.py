#!/usr/bin/python3
import requests
import json
from time import sleep
from random import randint
from tabulate import tabulate

API_KEY = "<ADD-HAVEIBEENPWNED-KEY-HERE>"
BREACH_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"
PASTE_URL = "https://haveibeenpwned.com/api/v3/pasteaccount/"

headers = {
    "hibp-api-key": API_KEY,
    "User-Agent": "PwnedHunter.v1"
}

def BreachHunter(accounts):
    breached_data = []
    for account in accounts:
        resp = requests.get(f"{BREACH_URL}{account}?truncateResponse=false", headers=headers)
        if resp.status_code == 200:
            r = resp.json()
            for data in r:
                date = data["BreachDate"]
                breach = data["Title"]
                breached_data.append([account,breach, date])
        sleep(randint(3,7))
    print (tabulate(breached_data, headers=["Breached Account", "Breach Title", "Breach Date"], tablefmt="github"))
    print ("\n")

def PasteHunter(accounts):
    pasted_data = []
    for account in accounts:
        resp = requests.get(f"{PASTE_URL}{account}", headers=headers)
        if resp.status_code == 200:
            r = resp.json()
            for data in r:
                source = data["Source"]
                id = data["Id"]
                date = data["Date"]
                pasted_data.append([account, source, id, date])
        sleep(randint(3,7))
    print (tabulate(pasted_data, headers=["Pasted Account", "Paste Source", "Paste ID", "Paste Date"], tablefmt="github"))
    print ("\n")

def PwnHunter(accounts):
    BreachHunter(accounts)
    paste_data = PasteHunter(accounts)
