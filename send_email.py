import smtplib, getpass

# Connect to server
server_address = 'smtp.gmail.com:587'
print('Connecting to', server_address)
server = smtplib.SMTP(server_address)  
print('Starting TLS')
server.starttls()  

# Credentials (if needed)  
username = input('User > ')  
password = getpass.getpass('Pass > ')  

print('Logging in')
server.login(username,password)  

fromaddr = input('From > ')
toaddrs  = input('To   > ')  
msg = input('Mesg > ')  

# The actual mail send  
print('Sending mail')
server.sendmail(fromaddr, toaddrs, msg)  
print('Done')
server.quit()  

