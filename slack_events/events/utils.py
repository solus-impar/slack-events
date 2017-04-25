import re
import sys
import requests


def events(c):
    """Identify a callable as events."""
    c.__events__ = " ".join(w.title() for w in uncamel(c.__name__).split('_'))
    c.__events__ = re.sub('Wwucs', 'WWUCS', c.__events__)
    c.__events__ = re.sub('Acm', 'ACM', c.__events__)
    c.__events__ = re.sub('Awc', 'AWC', c.__events__)
    return c() if type(c) is type else c


def uncamel(s):
    """
    Convert CamelCase class names into lower_snake_case.
    Taken from http://stackoverflow.com/a/1176023/3288364
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def fetch_json(url):
    """Fetch data from a URL and attempt to parse it as JSON."""
    error = "slack-events: error: {}"
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        sys.exit(error.format(
            "cannot connect to {}".format(url)
        ))

    status_code = response.status_code
    if status_code == 200:
        try:
            return response.json()
        except ValueError:
            sys.exit(error.format(
                "invalid JSON at {}".format(url)
            ))
    else:
        sys.exit(error.format(
            "{} fetching {}".format(status_code, url)
        ))
