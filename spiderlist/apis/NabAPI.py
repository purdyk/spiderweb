from django.conf import settings

import urllib.request
import urllib.parse
import json


class NabAPI:
    def __init__(self, filter_re):
        self.filter = filter_re

    def do_search(self, match_spec, offset):
        results = []

        q = "+".join(match_spec)

        params = {
            "apikey": settings.NEWZNAB_KEY,
            "t": "search",
            "o": "json",
            "q": q,
            "cat": "6000",
            "offset": offset}
        print("Match Spec: %s" % (q))
        finurl = "%s/api?%s" % (settings.NEWZNAB_URL, urllib.parse.urlencode(params))
        print("Fetching: %s" % finurl)
        with urllib.request.urlopen(finurl) as fh:
            data = json.loads(fh.read().decode('utf-8'))

            for thing in data:
                if not isinstance(thing, dict):
                    continue

                result = NabResult(thing)
                match = self.filter.search(result.title())

                if match:
                    result.set_date_key(".".join(match.groups()[-3:]))
                    results.append(result)

            return results


class NabResult:

    def __init__(self, attrs):
        self.attrs = attrs

    def size(self):
        return self.attrs['size']

    def title(self):
        return self.attrs['searchname']

    def guid(self):
        return self.attrs['guid']

    def date_key(self):
        return self.attrs['date_key']

    def set_date_key(self, key):
        self.attrs['date_key'] = key

    def __str__(self):
        return "{0}  --  {1}".format(self.title(), self.size_s)
