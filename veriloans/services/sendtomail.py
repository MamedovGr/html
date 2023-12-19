import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# smtp server value attributes
SERVER = 'smtp.yandex.com'
USER = 'agajanh@trl.gov.tm'
PASSWORD = 'HtrN&@MSEq?8m-V'

# Recipient address list, supports up to 30 recipients
rcptlist = ['atashew27@gmail.com', 'miulivenew1@gmail.com']
receivers = ','.join(rcptlist)

# Build multipart mail message
msg = MIMEMultipart('mixed')
msg['Subject'] = 'SQL Backup'
msg['From'] = USER
msg['To'] = receivers

# Build text/plain part of multipart/alternative
alternative = MIMEMultipart('multipart')
textplain = MIMEText ('SQL Backup')
alternative.attach(textplain)

# Add alternative into mixed
msg.attach(alternative)

# Attachment type
# xlsx type attachment
xlsxpart = MIMEApplication(open('/var/www/html/veriloans/services/backup.sql', 'rb').read())
xlsxpart.add_header('Content-Disposition', 'attachment', filename='backup.sql')
msg.attach(xlsxpart)

# Send mail
try:
    email = USER
    password = PASSWORD
    # server = smtplib.SMTP()
    # SSL may be needed to create a client in python 2.7 or later
    server = smtplib.SMTP_SSL(SERVER)
    # server.starttls()
    server.connect('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    # Sender has to match the authorized address
    server.sendmail(email, rcptlist, msg.as_string())
    server.quit()
    print('Email delivered successfully!')
# except smtplib.SMTPRecipientsRefused:
#     print('Email delivery failed, invalid recipient')
# except smtplib.SMTPAuthenticationError:
#     print('Email delivery failed, authorization error')
# except smtplib.SMTPSenderRefused:
#     print('Email delivery failed, invalid sender')
except smtplib.SMTPException as e:
    print('Email delivery failed', e)
