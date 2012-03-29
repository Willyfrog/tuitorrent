import twitter
from config import *

api = twitter.Api(consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET)

statuses = api.GetPublicTimeline()
print [s.user.name for s in statuses]
