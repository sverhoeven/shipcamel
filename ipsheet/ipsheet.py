import netifaces as ni
import json
import gspread
import threading
from oauth2client.client import SignedJwtAssertionCredentials

# connect to spreadsheet
json_key = json.load(open('/Users/mkuzak/Downloads/ipsheet-e54e6f9a4d37.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                                            json_key['private_key'],
                                            scope)
gc = gspread.authorize(credentials)

wks = gc.open("ipsheet").sheet1

# get ip address
eth0 = ni.ifaddresses('lo0')
ip_address = eth0[2][0]['addr']

# check if this ip address is already in the spreadsheet,
# if it's not append it to the column
try:
    wks.find(ip_address)
    # this is fine ip adress is already there
except:
    # append the address
    wks.update_cell(len(wks.col_values(1)) + 1, 1, ip_address)

# need to querry spreadsheet(for example every 10s)
# when key is pasted pick it up and stop queries
def fetch_key():
    cell = wks.find(ip_address)
    key = wks.cell(cell.row, 2).value
    if (key == ""):
        # querry again
        print("waiting for input")
        threading.Timer(0.5, fetch_key).start()
    else:
        # add the key
        print(key)

fetch_key()
