import smtplib
from email.message import EmailMessage
import imghdr
from os import listdir
import datetime

"""GLOBAL VARIABLES"""
YOUR_MAIL = '...'
YOUR_PASSWORD = '...'
RECIEVER_MAIL = '...'
IMGS_PATH = 'C:\\Users\\...\\graphics'
"""----------------"""

def start():
	if '...' in YOUR_MAIL:
		print('You havent set up your personal information')
	else:
		main()

def main():
	#local variables
	today = datetime.date.today()
	imgs = listdir(IMGS_PATH)
	
	#build mail
	msg = EmailMessage()
	msg['From'] = YOUR_MAIL
	msg['To'] = RECIEVER_MAIL
	msg['Subject'] = 'Product updates of ' + str(today)
	
	#add a html header
	msg.add_alternative("""
		<!DOCTYPE html>
		<html>
			<body>
				<h1 style="color:Red;"
					align="center">Product updates of """ + str(today) + """</h1>
			</body>
		</html>
		""", subtype='html')
	
	#add the graphics of your product prices
	for img in imgs:
		with open(IMGS_PATH + '\\' + img, 'rb') as f:
			file_data = f.read()
			file_type = imghdr.what(f.name)
			file_name = f.name
		msg.add_attachment(file_data, maintype='image', subtype=file_type, filename='image')
	
	#send it
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(YOUR_MAIL, YOUR_PASSWORD)
		smtp.send_message(msg)

if __name__ == '__main__':
	start()
