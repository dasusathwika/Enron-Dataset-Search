import mailbox
import sys
import email
import os
import glob
import shutil

'''
Function to search for given terms in messages. Takes mbox file path and the term list as parameters. 
Iterates over the given path to read all the files.
'''
def termSearch(mboxfilepath, terms):
    messages = []
    count=0
    s = ""
    for mboxfilename in mboxfilepath:
        mboxfile = mailbox.mbox(mboxfilename)
        for i, message in enumerate(mboxfile):
            flag = 0
            # '''is_multipart() return true if the message is a string an gets content of the message.
            # Else the message is converted to string'''
            if message.is_multipart():
                messagecontent = ''.join(part.get_payload(decode=True) for part in message.get_payload())
            else:
                messagecontent = str(message.get_payload(decode=True))

            # Checks if all the terms in the term list are present in the message content '''
            for term in terms:
                if not term in messagecontent.lower():
                    flag = 1
                    break

            # Prints the message if all the terms are present in the list
            if flag != 1:
                if type(message['X-From']) != type(s):
                    s = str(message['X-From'])
                    m = (str(count+1)+". "+s + " <" + message['from'] + ">  " + message['date'])
                    messages.append(m)
                    count+=1
                    print(m)
                    print(1)
                else:
                    m = (str(count+1)+". "+message['X-From'] + " <" + message['from'] + ">  " + message['date'])
                    messages.append(m)
                    count+=1
                    print(m)
    return messages

def emailAddress(mboxfilepath, firstname, lastname):
    name = []
    name.append(firstname)
    name.append(lastname)
    mails = []
    count = 0
    s = ""

    for mboxfilename in mboxfilepath:
        mbox = mailbox.mbox(mboxfilename)
        for i, message in enumerate(mbox):
            flag = 0
            from_address = message['X-From']
            for l in name:
                '''print(i)
                print(from_address)'''
                if from_address is not None and type(from_address) == type(s):
                    if not l in from_address.lower():
                        flag = 1
                        break
                elif from_address is None or type(from_address) != type(s):
                    flag = 1
                    break
            if flag != 1 and (not message['from'] in mails):
                mails.append(message['from'])
                print(str(count + 1) + ". " + mails[count])
                count += 1
    print("Results found: " + str(count))

def emailsExchanged(mboxFilePath, email1, email2):
    messages = []
    count = 0
    for mboxFileName in mboxFilePath:
        mbox = mailbox.mbox(mboxFileName)
        for i, message in enumerate(mbox):
            if (message['from'] == email1 and message['to'] == email2):
                messages.append(message)
                print(
                    str(count + 1) + ". " + email1 + " --> " + email2 + " [Subject: " + message['subject'] + "] " + message[
                        'date'])
                count += 1
            elif (message['from'] == email2 and message['to'] == email1):
                messages.append(message)
                print(
                    str(count + 1) + ". " + email2 + " --> " + email1 + " [Subject: " + message['subject'] + "] " + message[
                        'date'])
                count += 1

    print("Results found: " + str(count))

'''Converts the string to a list of strings by tokenizing them and converting to lower case'''
def modifyString(inp):
    inp = inp.lower()
    termlist = []
    terms = inp.split()
    for term in terms:
        # If condition is used to store unique string
        # in another list 'k'
        if (terms.count(term) >= 1 and (term not in termlist)):
            termlist.append(term)
    return termlist

folders = []
path = []
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("C:\\Users\\dasus\\enron1"):
    # print(files)
    if files:
        for file in files:
            path.append(root + "\\" + file)

s1 = "enron_search term_search "
s2 = "enron_search address_search "
s3 = "enron_search interaction_search "
inp = input()

# Checks if the command line arguments contains string s1
if s1 in inp:
    term = inp.replace(s1, "")
    k = modifyString(term)
    messages = termSearch(path, k)
    print("Results found: " + str(len(messages)))

# Checks if the command line arguments contains string s2
elif s2 in inp:
    term = inp.replace(s2, "")
    k = modifyString(term)
    # for i in path:
    emailAddress(path, k[0], k[1])

# Checks if the command line arguments contains string s3
elif s3 in inp:
    term = inp.replace(s3, "")
    k = modifyString(term)
    emailsExchanged(path, k[0], k[1])
