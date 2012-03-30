import twitter
from time import sleep, time
from config import *
import urllib
import re

URL_PATTERN = "((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(\/\S*)?)"


class TuitBot:
    def __init__(self, cons_key, cons_secret, token_key, token_secret):
        '''
        inicializacion, requiere los parametros proporcionados por
        dev.twitter.com
        '''
        self.cons_key = cons_key
        self.cons_secret = cons_secret
        self.token_key = token_key
        self.token_secret = token_secret
        self.api = twitter.Api(consumer_key=self.cons_key,
            consumer_secret=self.cons_secret,
            access_token_key=self.token_key,
            access_token_secret=self.token_secret)
        self.running_since = time()
        self.last_id = None
        self.saludar()

    def saca_urls(self, texto):
        '''dado un string saca las urls que haya'''
        patron = re.compile(URL_PATTERN)
        urls = patron.findall(texto)
        return [u[0] for u in urls]

    def actuar(self, estado):
        '''actua en base a la accion solicitada'''
        #TODO: meter plugins de acciones diferentes
        urls = self.saca_urls(estado.text)
        print "%s: %s" % (estado.user.name, ','.join(urls))

    def menciones(self):
        '''analiza las menciones al usuario'''
        print "leyendo menciones"
        try:
            mentions = self.api.GetMentions(since_id=self.last_id)
        except TwitterError as te:
            print "Error al recuperar el timeline: %s" % te.message
        if mentions:
            for m in mentions:
                if m.GetCreatedAtInSeconds() >= self.running_since:
                    self.actuar(m)
            self.last_id = mentions[0].GetId()
        else:
            print "sin menciones"

    def saludar(self):
        try:
            self.api.PostUpdate('Croack! [%s]' % self.running_since)
        except twitter.TwitterError as te:
            print "Error al saludar, tenemos permiso? %s" % te.message

    def expandir_url(self, url):
        resp = resp = urllib.urlopen(url)
        if resp.getcode() == 200:
            urlres = resp.url
        else:
            urlres = url
        return urlres

    def download(self, url):
        """Copy the contents of a file from a given URL
        to a local file.
        """
        try:
            webFile = urllib.urlopen(url)
            localFile = open(url.split('/')url[-1], 'w')
            localFile.write(webFile.read())
        except IOError as io:
            print "Archivo no disponible para descarga: %s" % io.message
        finally:
            webFile.close()
            localFile.close()

    def run(self):
        '''Ejecucion permamente'''
        while 1:
            self.menciones()
            sleep(REFRESH)  # TODO: extraer parametro a config

if __name__ == '__main__':
    t = TuitBot(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    t.run()

#TODO: comprobar que hay fichero de configuracion y parametros necesarios
#TODO: testing
#TODO: docs
#TODO: plugins
