from django.conf import settings

from urllib import request
from urllib import parse


class SabAPI:

    def enqueue(self, url, title):
        params = {
            "apikey": settings.SABNZBD_KEY,
            "mode": "addurl",
            "name": url,
            "cat": "xxx",
            "nzbname": title.replace(" ", "_")
            }

        finurl = "%s/api?%s" % (settings.SABNZBD_URL, parse.urlencode(params))

        print(finurl)

        fh = request.urlopen(finurl)
        res = fh.read().decode('utf-8')
        fh.close()
        return res