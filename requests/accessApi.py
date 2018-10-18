import donTFRequestor

resp = donTFRequestor.get_all('month')
if resp.status_code != 200:
	raise ApiError('Cannot fetch all donors by timeframe': {}'.format(resp.status_code))

for donorNum_Item in resp.json():
	print('{} {} {}'.format(donorNum_Item['regionID'], donTFRequests['locationName'], donTFRequests['numDonors']))