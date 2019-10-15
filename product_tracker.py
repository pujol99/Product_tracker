import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def main():
	f = open('database\products_url.txt', 'r')	#get all urls in a list
	urls = [url.rstrip('\n') for url in f]
	f.close()

	for url in urls:
		title = url.split('/')[3][:25] 	#get title from url
		path_prices = 'database\\' + title + '.txt' #build path for prices history
		
		if 'pccomponentes' in url:
			#find price inside pccomponentes
			response = requests.get(url)
			soup = BeautifulSoup(response.text, 'html.parser')
				
			container = soup.find('div', {'class':'ficha-producto__encabezado white-card-movil'})
			price = container.find('span', {'class':'baseprice'})
			if price is None:
				price = container.find('div', {'id':'precio-main'})
			price = price.get_text()

		elif 'amazon' in url:
			#find price inside amazon page, special 
			headers = {
				"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
			response = requests.get(url, headers=headers)
			soup = BeautifulSoup(response.content, "html.parser")
			soup = BeautifulSoup(soup.prettify(), "html.parser")
			
			price = soup.find(id= "priceblock_ourprice")
			price = price.get_text()[:-5]
		
		#add price to the history & create graphic with all data
		prices = write_data(path_prices, price)
		create_graphic(prices, title)

def write_data(path_prices, last_price):
	f = open(path_prices, 'a+')	#Add data
	f.write(last_price + '\n')
	f.close()
	
	f = open(path_prices, 'r')	#Return data
	prices = [price.rstrip('\n') for price in f]
	f.close()
	return prices

def create_graphic(prices, title):
	path_img = 'graphics\\' + title + '.png' #build path for prices images
	
	#create plot for image
	plt.title(title)
	plt.plot(prices)
	plt.savefig(path_img)
	plt.close()
	
if __name__ == '__main__':
	main()
