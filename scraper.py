import requests
from bs4 import BeautifulSoup
from datetime import datetime
from elasticsearch import Elasticsearch
import time
time.sleep(20)

try:
	es = Elasticsearch(host="es01", port=9200, timeout=30, max_retries=10, retry_on_timeout=True)
	if not es.ping():
		raise Exception("error in connecting to elasticsearch")
	else:
		print("connected")

	for season in range(2008, 2020):

		result = requests.get("http://www.howstat.com/cricket/Statistics/IPL/SeriesMatches.asp?s="+str(season))

		src = result.content
		soup = BeautifulSoup(src, 'lxml')

		for match in soup.find_all("table", {"class": "TableLined"}):
			
			tr = match.find_all("tr")
			for item in tr[1:]:
				# print(item)
				td_list = []
				for td in item.find_all("td"):
					td_list.append(td)
				# print(td_list)

				date = td_list[0].string.strip()
				
				a = item.find("a", {"class": "LinkNormal"})
				url = "http://www.howstat.com/cricket/Statistics/IPL/"+ a.attrs['href'].strip()
				team1 = a.string.split(':')[1].split('v')[0].strip()
				team2 = a.string.split(':')[1].split('v')[1].strip()

				location = td_list[2].string.strip()
				if td_list[3].span:
					winner= td_list[3].span.string
					won_by =  td_list[3].span.string
				elif td_list[3].string.strip().startswith('Match tied'):
					winner='Match tied'
					won_by='Super Over'
				else:
					# print(td_list[3].string)
					winner = td_list[3].string.split('won by')[0].strip()
					won_by = td_list[3].string.split('won by')[1].split()[1].strip()
				
				won_by_wkt,won_by_run=0,0

				if won_by.startswith('Wicket'):
					won_by_wkt = td_list[3].string.split('won by')[1].split()[0].strip() 
				elif won_by.startswith('Run'):
					won_by_run = td_list[3].string.split('won by')[1].split()[0].strip() 

				
				# print('URL:', url)

				match_result = requests.get(url)
				match_src = match_result.content
				match_soup = BeautifulSoup(match_src, 'lxml')
				# print(match_soup)
				
				more_details = match_soup.find_all("td", {"class":"TextBlack8"})
				# print(more_details)

				
				# if won_by.startswith('Wicket'):
					# print('Won By:', won_by_wkt, won_by)
				# else:
					# print('Won By:', won_by_run, won_by)
				
				venue = more_details[1].string.strip()
				# print('Venue:', venue)
				toss = more_details[3].string.strip()
				# print('Toss:', toss)
				mom = more_details[5].string.strip()
				# print('MOM:', mom)
				# print(len(soup.find_all("table")))

				print()

				doc = {
				    'season': str(season),
				    'match': a.string.split(':')[0].strip(),
				    'game_date': date,
				    'location:': location,
				    'venue':venue,
				    'team1':team1,
				    'team2':team2,
				    'winner':winner,
				    'won_by':won_by,
				    'won_by_wkt': won_by_wkt,
				    'won_by_run': won_by_run,
				    'toss':toss,
				    'mom':mom,
				    'timestamp': datetime.now(),
				}
				print(doc)

				res = es.index(index="matches", body=doc)
				print(res['result'])

				print()
			
except Exception as e:
	print(e)
