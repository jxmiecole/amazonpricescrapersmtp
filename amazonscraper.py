import requests
from bs4 import BeautifulSoup as bs
import smtplib
import time

#paste url of your product here
URL = 'https://www.amazon.co.uk/Apple-Watch-Space-Aluminium-Black/dp/B08J676WX8/ref=sr_1_3?dchild=1&keywords=apple+watch&qid=1610098840&sr=8-3'
#paste your user agent here by googling "My user agent"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

def FindData():
	page = requests.get(URL, headers=headers)
	soup = bs(page.content, 'html.parser')
	title = soup.find(id="productTitle").text
	price = soup.find(id="priceblock_ourprice").text
	converted_price = (price[1:4])

	if(int(converted_price) < 360):
		sendMail()

def sendMail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login('testdatasendingsmtp', 'cnggkrouamtmskge')

	title = bs(requests.get(URL, headers=headers).content, 'html.parser').find(id="productTitle").text
	condensed_title = (title[8:28])
	subject = ('Price has fallen on the', condensed_title)
	body = ('This is the link:', URL)

	msg = f"Subject: {subject}\n\n{body}"

	sender = 'testdatasendingsmtp@gmail.com'
	reciever = 'youremail@gmail.com'

	server.sendmail(
		sender,
		reciever,
		msg 
	)
	print("The Email Has been sent as the price has dropped.")

	server.quit()

while(True):
	FindData()
	#checks every 12 hours for price change
	time.sleep(43200)
