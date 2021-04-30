import imaplib
import email
import json
from getpass import getpass
from email.header import decode_header
import webbrowser
import os
import re


# https://gocovri-hcp-banner.fcbstage.com
# UN: adfafdsdfasfd
# PW: asdfasdfasfdasfd

# {
#   "last_message_id": 16061,
#   "stage_links": [
#       {
#           url: "",
#           un: "",
#           pw: ""
#       },
#   ]
# }




def find_urls(string):
    regex = r'(?=.*fcbstage.com)(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
    urls = []
    matches = re.finditer(regex, string)
    for match in matches:
        urls.append(match.group(0))

    return list(set(urls))


def email_auth():
    username = input()
    password = getpass('EMAIL: ' + username + '\n' + 'PASSWORD: ')
    imap = imaplib.IMAP4_SSL('imap.gmail.com')  # create an IMAP4 class with SSL
    # imap = imaplib.IMAP4_SSL('imap-mail.outlook.com')
    imap.login(username, password)  # log in with credentials

    return imap


def init():
    # User Authentication
    imap = email_auth()
    # Get list of message IDs as raw bytes from inbox
    status, total_messages = imap.select('INBOX')
    # Check status
    print('\nSTATUS: ' + status)
    # decode message
    last_message_id = int(total_messages[0].decode('utf-8'))
    # init stage url list
    stage_links = []

    # get json file
    file_path = 'index.json'
    # open json file
    if os.path.isfile(file_path):
        # try to parse value
        with open(file_path, 'r') as file_handle:
            # retrieve the value
            data = json.load(file_handle)
            # check if value is there
            if 'last_message_id' in data:
                # set starting point to read from
                first_message_id = data['last_message_id'] + 1
            else:
                # set how many emails to read
                num_messages_to_scan = int(input('NUMBER OF EMAILS: '))
                # set starting point by default
                first_message_id = last_message_id - num_messages_to_scan

    # check ids before work
    print("first_message_id: ", first_message_id)
    print("last_message_id:  ", last_message_id)


    # do work..
    for message_id in range(first_message_id, last_message_id + 1):
        # Fetch the email message by ID
        result, message = imap.fetch(str(message_id), '(RFC822)')
        for response in message:
            try:
                # Parse bytes into email object then into a string
                body = email.message_from_bytes(response[1])
                body = email.message.Message.as_string(body)
                # retrieve urls in the email body
                urls = find_urls(body)
                if urls:
                    # append new urls to json
                    stage_links.append(urls)

            except:
                pass

    else:
        # once for loop is done ...
        print("\nWRITING TO FILE")
        # package last id and stage urls into data
        data = {
            "last_message_id": last_message_id,
            "stage_links": stage_links
        }
        print(json.dumps(data))
        # write data to disk
        with open(file_path, 'r+') as file_handle:
            file_handle.truncate(0)
            file_handle.write(json.dumps(data))
            file_handle.close()

    # Close the connection
    imap.close()
    # Logout
    imap.logout()


init()

# COREY'S EXAMPLE CODE FOR LOADING JSON
#
# import os
# import json
#
# data = {}
#
# # query imap for last_message_id
# last_message_id = 17061
# first_message_id = last_message_id - 100
#
# file_path = 'index.json'
# if os.path.isfile(file_path):
#     with open(file_path, 'r') as file_handle:
#         data = json.load(file_handle)
#         if 'last_message_id' in data:
#             first_message_id = data['last_message_id'] + 1
#
# #if first_message_id > last_message_id:
# #   return
#
# print('Reading e-mails from index {0} to {1}'.format(first_message_id, last_message_id))
# # do work, read emails, get urls, save them to files, whatever
#
#
# data['last_message_id'] = last_message_id
#
# with open(file_path, 'w') as file_handle:
#     json.dump(data, file_handle)
