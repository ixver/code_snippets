
import os, sys

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../_elements/'))

from xos import *
from xpd import *
from xpk import *
from __utils import *

'''	SOME I WROTE CODE TO SCRAPE MULTIPLE WEBSITES AND UPDATE EXISTING DATA '''

def update_state_values(states):

	states['drivers'] = {
		'chrome': os.environ['CHROMEDRIVER_PATH'],
		'firefox': os.environ['FIREFOXDRIVER_PATH'],
	}

	states['scrapes']['queues']['websitecategory'] = {

		'websiteA': [
			'https://www.website.com/en-us/category/domain.html',
		],
		'websiteB': [
			'https://www.website.com/en-us/category/domain.html',
		],
		'websiteC': [
			'https://www.website.com/en-us/category/domain.html',
		],
		'websiteD': [
			'https://www.website.com/en-us/category/domain.html',
		],
	}

	return states

def translate_soup(key, soup):

	cols = []
	vals = []
	if (key == 'websiteA'):
		rows = soup.find_all('tr', attrs={'class': 'classname'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']
		df1 = pd.DataFrame(np.array(vals), columns=cols)
		return df1.copy()
	elif (key == 'websiteB'):
		rows = soup.find_all('tr', attrs={'class': 'table__some-numbers'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']
		df1 = pd.DataFrame(np.array(vals), columns=cols)
		return df1.copy()
	elif (key == 'websiteC'):
		rows = soup.find_all('tr', attrs={'data-toggle': 'sometable'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[4].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']
	elif (key == 'websiteD'):
		rows = soup.find_all('tr', attrs={'data-toggle': 'sometable'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[4].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']
	elif (key == 'websiteE'):
		rows = soup.find_all('tr', attrs={'data-toggle': 'sometable'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[4].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']
	elif (key == 'websiteF'):
		rows = soup.find_all('tr', attrs={'data-toggle': 'sometable'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[4].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']
	elif (key == 'websiteG'):
		rows = soup.find_all('tr', attrs={'data-toggle': 'sometable'})
		for row in rows:
			_nr = []
			_nr.append(row.find('td', attrs={'title': 'date'}).contents[0])
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[0].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[1].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[2].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[3].text)
			_nr.append(row.find('div', attrs={'class': 'somearea-subarea'}).find_all('span')[4].text)
			vals.append(_nr)
		cols = ['timestamp', 'a', 'b', 'c', 'd', 'e']

	if (len(vals)):
		df1 = pd.DataFrame(np.array(vals), columns=cols)
		return df1.copy()
	else:
		return None

def get_soup(url):

	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from time import sleep

	from webdriver_manager.chrome import ChromeDriverManager


	options = Options()
	options.add_argument("--headless")

	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


	# get url content, using seleniUm
	sleep(1)
	driver.get(url)
	sleep(2)

	# convert data
	soup = BeautifulSoup(driver.page_source, 'lxml')
	driver.close()
	driver.quit()

	return soup

def x(states, it):

	print('\n# scrapes are in progress...')

	vals = states['scrapes']['queues']['somearea'][it]

	''' existing '''
	states = update_state_values(states)
	exist_df = load_div_data(states, 'source')
	print('\t. existing')
	print('\t\t...')
	print(exist_df.tail(4))
	print('\t\t...')

	''' request '''
	for url in vals:
		soup = get_soup(url)

		''' new '''
		new_df = translate_soup(it, soup)
		print('\t. new')
		print('\t\t...')
		print(new_df.tail(4))
		print('\t\t...')

		''' update existing with new '''
		if (exist_df is None):
			updated_df = new_df.copy()
		else:
			index_c = 'timestamp'
			updated_df = update_df(exist_df, new_df, index=index_c)
			updated_df.sort_values(by=index_c, inplace=True)
		print('\t. updated')
		print('\t\t...')
		print(updated_df.tail(4))
		print('\t\t...')

		''' save '''
		save_div_data(states, 'source', updated_df)

	print('\n. {} is done.'.format(it))

	return states

