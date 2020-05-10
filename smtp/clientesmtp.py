import smtplib
import email.utils
from email.mime.text import MIMEText

host = '127.0.0.1'
port = 1025

msg = MIMEText('Hola Mundo')
msg['To'] = email.utils.formataddr(('Recipiente', 'servidorP@mail.com'))
msg['From'] = email.utils.formataddr(('Autor', 'zabdiel@mail.com'))
msg['Subject'] = 'Prueba de correo electronico por SMTP'

server = smtplib.SMTP(host,port)
server.set_debuglevel(True)
try:
    server.ehlo_or_helo_if_needed()
    server.send_message(msg,"zabdiel@mail.com", "servidorP@mail.com")
    #server.sendmail("zabdiel@mail.com","servidorP@mail.com",msg.as_string())
finally:
    server.quit()