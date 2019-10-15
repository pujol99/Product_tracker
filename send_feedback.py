import smtplib
from email.message import EmailMessage
import imghdr
from os import listdir
import datetime

today = datetime.date.today()

email = 'alexpujolcomet@gmail.com'
password = 'incorrecta'

to = ['alexpujolcomet8@gmail.com']

msg = EmailMessage()
msg['From'] = email
msg['To'] = to
msg['Subject'] = 'Product updates of ' + str(today)

msg.add_alternative("""
	<!DOCTYPE html>
	<html>
		<body>
			<h1 style="color:SlateGray;"
				align="center">Product updates of """ + str(today) + """</h1>
		</body>
	</html>
	""", subtype='html')

imgs_path = 'C:\\Users\\Alex\\OneDrive\\Projects\\Products\\graphics'
imgs = listdir(imgs_path)

i = 1
for img in imgs:
	with open(imgs_path+ '\\' + img, 'rb') as f:
		file_data = f.read()
		file_type = imghdr.what(f.name)
		file_name = f.name
		
	msg.add_attachment(file_data, maintype='image', subtype=file_type, filename='image'+str(i))
	i += 1

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	smtp.login(email, password)
	
	smtp.send_message(msg)