import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import datetime

TODAY = str(datetime.date.today())
HEADERS = {
	"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}


def main():
	f = open('database\products_url.txt', 'r')	#open your urls file
	urls = [url.rstrip('\n') for url in f]		#put them in a list
	f.close()									

	for url in urls:
		title = url.split('/')[3][:25] 						#get title from url
		path_prices = 'database\\' + title + '.txt' 		#build path for prices history
		
		response = requests.get(url, headers=HEADERS)		#get page content
		soup = BeautifulSoup(response.text, 'html.parser')
		
		if 'pccomponentes' in url:							#find price inside PCCOMPONENTES	
			container = soup.find('div', {'class':'ficha-producto__encabezado white-card-movil'})
			price = container.find('span', {'class':'baseprice'})
			if price is None:
				price = container.find('div', {'id':'precio-main'})
			price = price.get_text()

		elif 'amazon' in url:								#find price inside AMAZON
			soup = BeautifulSoup(soup.prettify(), 'html.parser')
			price = soup.find(id= 'priceblock_ourprice')
			price = price.get_text()[:-5]
		
		#add price to the history & create graphic with all data
		prices, days = write_data(path_prices, price)
		create_graphic(prices, days, title)

def write_data(path_prices, last_price):
	f = open(path_prices, 'a+')					#Add data to history file
	f.write(last_price + ' ' + TODAY + '\n')
	f.close()
	
	f = open(path_prices, 'r')					#Return all data
	data = [price.rstrip('\n') for price in f]
	f.close()
	
	prices = []
	days = []	
	for d in data:
		temp = d.split()
		prices.append(int(temp[0]))
		days.append(temp[1])
	
	return prices, days

def create_graphic(prices, days, title):
	path_img = 'graphics\\' + title + '.png' #build path for prices images
	
	#create plot for png image
	plt.title(title)
	plt.plot(days, prices)
	plt.xlabel('Price')
	plt.ylabel('Datetime')
	plt.savefig(path_img)
	plt.close()
	
if __name__ == '__main__':
	main()
