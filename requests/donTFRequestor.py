import requests

def _url(path):
    return 'https://localhost:5000/api' + path

def get_all(timeframe):
	if timeframe == 'month':
		return requests.get(_url('/monthlyDonors/'))
	elif timeframe == 'day':
		return requests.get(_url('/dailyDonors/'))
	else:	
		return requests.get(_url('/monthlyDonors/'))
		
def get_timeframe(timeframe, date_num):
	if timeframe == 'month':
		return requests.get(_url('/monthlyDonors/{:d}/'.format(date_num)))
	elif timeframe == 'day':
		return requests.get(_url('/dailyDonors/{:d}/'.format(date_num)))
