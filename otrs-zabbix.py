import os
from pyzabbix import ZabbixAPI
import re
import ssl
from imapclient import IMAPClient
import email
import sys
 

HOST = 'mail.server'                           #IMAP SERVER
USERNAME = 'mail user'                     #IMAP username
PASSWORD = 'password'                                           #IMAP user password

eventid = sys.argv[1]                                                  #EventID argument from zbx

#Disable SSL check
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

with IMAPClient(HOST, ssl_context=ssl_context) as server:
    server.login(USERNAME, PASSWORD)
    select_info = server.select_folder('INBOX')
    messages = server.search(['SUBJECT', eventid])                  #Search zbx EventID in Subject
    for msgid, data in server.fetch(messages, 'RFC822').items():
        email_message = email.message_from_bytes(data[b'RFC822'])
        subj = email_message.get('Subject')
    server.logout()

os.environ['no_proxy'] = '*'                           #Avoid systemwide proxy if needed
#Set ACK without closing problem
zapi = ZabbixAPI('https://zabbix.server/zabbix')                                
zapi.session.verify = False                                                                                                                                        
zapi.login('Login', 'Password')
ack = zapi.event.acknowledge(
        eventids= eventid,
        message= subj[0:16],
        action=0
        )
