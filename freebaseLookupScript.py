import json
import urllib
from datetime import date


def get_new_books(favorite_authors):
    """
    (list) -> (list of lists)

    take a list of authors to be checked
    return a list of lists of type
    [[authors' names], date of publication, title of the book]
    containing info about books that are published
    by favorite_authors during the current month
    """
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'


    api_key = 'some_key'  #change api_key manually

    current_month = str(date(date.today().year, date.today().month, 1))
    next_month = str(date(date.today().year, date.today().month + 1, 1))
    response = []

    for mid in favorite_authors:
        query = [{
            "type": "/book/book",
            "name": None,
            "/book/written_work/author": [{"mid": mid}],
            "/book/written_work/date_of_first_publication>":
            "%s" % (current_month),
            "ns0:/book/written_work/date_of_first_publication<":
            "%s" % (next_month),
            "/book/written_work/date_of_first_publication": None,
            "ns0:/book/written_work/author": []
        }]

        params = {
            'query': json.dumps(query),
            'key': api_key
        }
        url = service_url + '?' + urllib.urlencode(params)
        response.append(json.loads(urllib.urlopen(url).read()))

    values = []

    for res in response:
        for i in res['result']:
            values.append([[str(a) for a in i['ns0:/book/written_work/author']],
                            str(i["/book/written_work/date_of_first_publication"]),
                            str(i['name'])])
    return values


class my_class(NebriOS):
    schedule = "0 0 * * *"

    def check(self):
        global new_releases
        favorite_authors = ['/m/0675ss', '/m/0jt90f5']
        all_new_releases = get_new_books(favorite_authors)
        new_releases = [book for book in all_new_releases \
            if book not in shared.favorite_author_releases]
        return bool(new_releases)

    def action(self):
        shared.favorite_author_releases += new_releases
