import requests
import json
import pandas as pd
import numpy as np
import smtplib

import time
from pandas import json_normalize 

def getfileReading():
    f = open("total_booking_count.txt", "r")
    txt=f.read()
    num=int(txt.strip())
    return num
def fileWriter(text):
    f = open("total_booking_count.txt", "w")
    f.write(text)
    f.close()   

def send_email_alert(gmail_user,gmail_password,to,email_text):
    sent_from = gmail_user


    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

def getTotalBooking():
    url = "https://backend.aayacare.com/iapi/v1/getbookingList"
    payload = json.dumps({
      "pageVo": {
        "pageNo": 2,
        "noOfItems": 1
      },
      "filterBooking": "all",
      "currentDate": 1668871300395
    })
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json',
      'Origin': 'http://35.154.45.30:7070',
      'Referer': 'http://35.154.45.30:7070/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'cross-site',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MWE5ZTU3NzAzNjU0MDYxMzY4ODlhY2UiLCJuYW1lIjoiYWRtaW4iLCJjb21wYW55X25hbWUiOiJBYXlhY2FyZSIsImVtYWlsIjoiYWRtaW5AYWF5YWNhcmUuY29tIiwicGhvbmUiOiIxMTExMTExMTExIiwicm9sZSI6MSwiaWF0IjoxNjY4ODY3OTczLCJleHAiOjE2NzkyMzU5NzN9.FO9NQuak_Vw_LAX509R8zmkFfpb43jeWFUwlO0a_Vrc'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    # json_data = json.loads(response)
    # print(json_data)
    json_response=response.json()
    # print(response.json())
    # print(response.text)

    df = json_normalize(json_response['data'])
    total_bookings=df['total'].squeeze()

    return total_bookings



# getTotalBooking()
# fileWriter(str(getTotalBooking()))
# fileReader()

def check_diff_count(a,b):
    if a!=b :
        return True
    return False

# print(check_diff_count(3,2))

def main():
    fileWriter("0")
    while True:
        prev_count=getfileReading()
        if(prev_count != 0 and check_diff_count(prev_count,getTotalBooking())):
            send_email_alert('info.aayacare@gmail.com','uysiwtebkakpncux',['info.aayacare@gmail.com', 'arunsathyan.sreyas001@gmail.com','vaishnavcraj@gmail.com'],'URGENT---New booking have been revieved through Aayacare application')

        
        total_bookings=str(getTotalBooking())
        fileWriter(total_bookings)
        time.sleep(10)
        

if __name__ == "__main__":
    main()












# send_email_alert('info.aayacare@gmail.com','uysiwtebkakpncux',['vaishnavcraj@gmail.com', 'arunsathyan.sreyas001@gmail.com'],'URGENT-New booking have been revieved through Aayacare application')

