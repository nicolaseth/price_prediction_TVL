# import coinmarketcapapi
# cmc = coinmarketcapapi.CoinMarketCapAPI('a1330e1e-8e84-4c06-af10-771d050574c4')
#
# #data = cmc.cryptocurrency_info(symbol='ONE')
# data = cmc.cryptocurrency_quotes_latest(symbol='ONE', convert='USD')
# print(data)

from requests import Request, Session
import json
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical"

parameters = {
    'slug':'bitcoin',
    'convert':'USD',
    'interval':'daily'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR KEY HERE',
}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)

print(json.loads(response.text))
