import requests
import urllib.request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def main():
	
	f = open('database\products_url.txt', 'r')
	urls = [url.rstrip('\n') for url in f]

	for url in urls:
		if 'pccomponentes' in url:
			title = url[30:55]
			
			response = requests.get(url)
			soup = BeautifulSoup(response.text, 'html.parser')
				
			container = soup.find('div', {'class':'ficha-producto__encabezado white-card-movil'})
			price = container.find('span', {'class':'baseprice'})
			if price is None:
				price = container.find('div', {'id':'precio-main'})
			
			path_hist = 'database\\' + title + '.txt'
			path_img = 'graphics\\' + title + '.png' 
			f = open(path_hist, 'a+')
			
			f.write(price.text)
			f.write('\n')
			
			f.close()
			
			create_graphic(path_hist, path_img, title)
		elif 'amazon' in url:
			title = url[22:40]
			
			headers = {
				"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
			}
			response = requests.get(url, headers=headers)
			soup = BeautifulSoup(response.content, "html.parser")
			soup = BeautifulSoup(soup.prettify(), "html.parser")

			price = soup.find(id= "priceblock_ourprice")
			price = price.get_text()[:-5]
			path_hist = 'database\\' + title + '.txt'
			path_img = 'graphics\\' + title + '.png' 
			f = open(path_hist, 'a+')
			
			f.write(price)
			f.write('\n')
			
			f.close()
			
			create_graphic(path_hist, path_img, title)
			

def create_graphic(path_hist, path_img, title):
	prices_data = []
	
	f = open(path_hist, 'r')
	prices = [price.rstrip('\n') for price in f]
	for price in prices:
		prices_data.append(price)
	prices_data.sort()
	
	plt.title(title)
	plt.plot(prices_data)
	plt.savefig(path_img)
	plt.close()
	
if __name__ == '__main__':
	main()