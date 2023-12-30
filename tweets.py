import pandas as pd
from ntscraper import Nitter
# query = "python"

scaper = Nitter()
tweets = scaper.get_tweets('mecskyverse', mode='user', number=-1, filters=["replies"])
print('pages are ',tweets)