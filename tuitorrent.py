import twitter
from datetime import datetime
from config import *
import urllib


class TuitBot:
    def __init__(self, cons_key, cons_secret, token_key, token_secret):
        self.cons_key = cons_key
        self.cons_secret = cons_secret
        self.token_key = token_key
        self.token_secret = token_secret
        self.api = twitter.Api(consumer_key=self.cons_key,
            consumer_secret=self.cons_secret,
            access_token_key=self.token_key,
            access_token_secret=self.token_secret)
        self.last_run = datetime.now()

    def actualizar(self):
        statuses = self.api.GetFriendsTimeline()
        for s in statuses:
            if 'http' in s.text:
                print "%s: %s" % (s.user.name, s.text)

    def saludar(self):
        try:
            self.api.PostUpdate('Croack!')
        except twitter.TwitterError as te:
            print "Error al saludar, tenemos permiso? %s" % te.message

    def expandir_url(self, url):
        resp = resp = urllib.urlopen(url)
        if resp.getcode() == 200:
            urlres = resp.url
        else:
            urlres = url
        return urlres

if __name__ == '__main__':
    t = TuitBot(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    t.saludar()
    t.actualizar()

