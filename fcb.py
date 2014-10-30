"""Check the ticket availability online and send an email when it's available.

   - Xue Feng 04/2014
   
"""
import urllib2
import smtplib, os, time
from email.mime.text import MIMEText
import requests

# Ticket url
ticket_url = 'https://tickets-fcb.fcbarcelona.com/fcbarcelona/en_US/entradas/evento/1004'
text_pre = 'title:"FC Barcelona - At. Madrid'
#text_pre = 'title:"FC Barcelona - Ath. Bilbao'
text_ticket = 'SOLD OUT'

def send_email():
    ''' send an email to myself.'''
    server_address = 'smtp.gmail.com';
    email_address = 'fengx03@gmail.com'
    passwd = '280115Yu'
    msg = MIMEText(ticket_url)
    msg['Subject'] = 'Tickets available!'
    msg['From'] = email_address
    msg['To'] = email_address

    server = smtplib.SMTP(server_address)
    server.starttls()
    server.login(email_address, passwd)
    server.sendmail(email_address, email_address, msg.as_string())
    server.quit()
    
if __name__ == '__main__':
    while 1:
        page = requests.get(ticket_url)
        start = page.text.find(text_pre)
        end = start + 200
        result = page.text.find(text_ticket, start, end)
        if result == -1:
            send_email()
            break
        time.sleep(600)
