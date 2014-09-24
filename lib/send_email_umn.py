#!/usr/bin/python3

import smtplib, getpass
from sys import exit

# Connect to server
server_address = 'smtp.gmail.com:587'
print('Connecting to', server_address)
server = smtplib.SMTP(server_address)  
print('Starting TLS')
server.starttls()  

# Credentials
fromname = input('Name > ')
username = input('x500 > ')  
password = getpass.getpass('Pass > ')  
fromaddr = username + '@umn.edu'

# Logging in
try:
    print('Logging in')
    server.login(fromaddr,password)  
except:
    print('Failed to log in.')
    print('Did you use your Google Desktop / Mobile Client Password?')
    server.quit()
    exit()

# Get message information
toaddrs = input('To      > ')
subject = input('Subject > ')
msg     = input('Message > ')  

# Compile the email body
msg = '\r\n'.join(['To: %s' % toaddrs,
                   'From: %s <%s>' % (fromname, fromaddr),
                   'Subject: %s' % subject,
                   '',
                   msg])


# The actual mail send
try:
    print('Sending mail')
    server.sendmail(username, toaddrs, msg)
    print('Done')
except:
    print('Error sending mail.')

server.quit()  

