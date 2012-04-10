import twitter
from time import sleep, time
from config import *
from urllib2 import urlopen, Request, unquote
import unicodedata
import re
import os.path

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
            access_token_secret=self.token_secret,
            input_encoding='utf8')
        self.running_since = time()
        self.last_id = None

    def saca_urls(self, texto):
        '''dado un string saca las urls que haya'''
        patron = re.compile(URL_PATTERN)
        urls = patron.findall(texto)
        return [u[0] for u in urls]

    def actuar(self, estado):
        '''actua en base a la accion solicitada'''
        #TODO: meter plugins de acciones diferentes
        urls = self.saca_urls(estado.text)
        #print "%s: %s" % (estado.user.name, ','.join(urls))
        for u in urls:
            m = self.download(self.expandir_url(u))
            self.escribir(m, estado.user.screen_name)

    def menciones(self):
        '''analiza las menciones al usuario'''
        print "leyendo menciones"
        try:
            mentions = self.api.GetMentions(since_id=self.last_id)
        except TwitterError as te:
            print "Error al recuperar el timeline: %s" % te.message
        if len(mentions):
            for m in mentions:
                if m.GetCreatedAtInSeconds() >= self.running_since:
                    self.actuar(m)
            self.last_id = mentions[0].GetId()
        else:
            print "sin menciones"

    def escribir(self, texto, id_user=''):
        '''
        escribe su estatus y si se le pasa un id lo hace mencionando al usuario
        '''
        l = len(id_user)
        user = ""
        if l:
            user = u"@%s" % id_user
        if len(texto) + l > 138:  # contar ademas un espacio y una @
            mensaje = u"%s %s" % (user,  texto[:138 - l])
        else:
            mensaje = u"%s %s" % (user, texto)
        try:
            self.api.PostUpdate(mensaje.encode('utf8'))
        except twitter.TwitterError as te:
            print "Error al escribir el mensaje: %s" % te.message

    def saludar(self):
        self.escribir(u"Croak %s" % self.running_since)

    def expandir_url(self, url):
        resp = resp = urlopen(url)
        if resp.getcode() == 200:
            urlres = resp.url
        else:
            urlres = url
        return urlres

    def download(self, url):
        """Copy the contents of a file from a given URL
        to a local file.
        """
        nombre = unquote(url.split('/')[-1])
        req = Request(url)
        r = urlopen(req)
        if ('Content-Disposition') in r.info():
            nombre = unquote(
                    r.info()['Content-Disposition'].split('filename=')[1])

        if nombre[0] == '"' and nombre[-1] == '"':
            # linux deja las comillas y macos no
            nombre = nombre[1:-1]
        # TODO: buscar si concuerda con un torrent una vez descargado
        f = open(os.path.join(PATH, nombre), 'wb')
        f.write(r.read())
        f.close()
        mensj = u"Descargando %s" % nombre
        return mensj

    def run(self):
        '''Ejecucion permamente'''
        self.saludar()
        while 1:
            self.menciones()
            sleep(REFRESH)

if __name__ == '__main__':
    t = TuitBot(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    t.run()

#TODO: comprobar que hay fichero de configuracion y parametros necesarios
#TODO: testing
#TODO: docs
#TODO: plugins
