"""events.callables module: plugins for slack-events.

Below is some of the requirements for plugins.

Args:
    None

Returns:
    message (str), channel (str): `message` should have information about
        the event formatted for posting to slack. `channel` can be empty
        for #general.

Raises:
    Not required, but use when needed.
"""
from datetime import date
import re
from bs4 import BeautifulSoup
import requests
from slack_events.events.utils import events


@events
def wwucs_events():
    """WWUCS events posted to cse.wwu.edu/computer-science."""
    error = "slack-events: error: {}"
    cse_url = "https://cse.wwu.edu"
    cs_url = "{}/computer-science".format(cse_url)
    cs_html = requests.get(cs_url)
    if not cs_html.ok:
        print(error.format("Could not connect to {}".format(cs_url)))
        return '', ''

    cs_soup = BeautifulSoup(cs_html.text, 'html.parser')
    today = date.today().strftime('%A, %B %d, %Y')
    todays_events = ''

    for link in cs_soup.find_all('a'):
        if 'event' in link['href']:
            event_html = requests.get(cse_url + link['href'])
            event_soup = BeautifulSoup(event_html.text, 'html.parser')
            event_date = event_soup.find('span', class_='date-display-single')
            location = event_soup.find('div', class_=re.compile('event-location'))
            if today in event_date.text:
                title = event_soup.title.text.strip()
                title = title[:title.rfind(' | '):]
                todays_events += "{}\n{}\n{}\n{}\n".format(
                    title,
                    event_date.text.strip(),
                    location.text.strip(),
                    cse_url + link['href']
                )

    return todays_events, ''


#TODO: 2017-02-23: Below are possible plugins for various WWUCS clubs and
#   associations. Since most events are posted to the WWUCS events page,
#   these plugins would be redundant at the moment.

'''
@events
def acm_events():
    """AWC events posted to acm.orgs.cs.wwu.edu."""
    error = "slack-events: error: {}"
    acm_url = 'http://acm.orgs.cs.wwu.edu'
    acm_html = requests.get(acm_url)
    if not acm_html.ok:
        print(error.format("Could not connect to {}".format(acm_url)))
        return '', ''

    acm_soup = BeautifulSoup(acm_html.text, 'html.parser')
    today = re.sub('Thu', 'Thurs', date.today().strftime('%a. %b %-d'))
    todays_events = ''

    for event in acm_soup.find_all('li', class_=re.compile('timeline')):
        event_date = event.find('div', class_='timeline-image')
        if today in event_date.h4.text:
            title = event.find('div', class_=re.compile('heading|title'))
            title = title.h4.text.strip()
            todays_events += "{}\n{}\n{}\n".format(
                title,
                event_date.h4.text.strip(),
                acm_url
            )

    return todays_events, ''


@events
def awc_events():
    """AWC events posted to awc.orgs.cs.wwu.edu."""
    error = "slack-events: error: {}"
    awc_url = 'http://awc.orgs.cs.wwu.edu'
    awc_html = requests.get(awc_url)
    if not awc_html.ok:
        print(error.format("Could not connect to {}".format(awc_url)))
        return '', ''

    awc_soup = BeautifulSoup(awc_html.text, 'html.parser')
    #TODO: 2017-03-23: No events posted, so unknown event identifiers.


@events
def cyber_security_events():
    """Cyber Security Club events posted to ???"""
    #TODO: 2017-03-23: No website for events.


@events
def game_design_events():
    """Game Design Club events posted to wwugamedevclub.github.io/event."""
    error = "slack-events: error: {}"
    gdc_url = 'http://wwugamedevclub.github.io/event'
    gdc_html = requests.get(gdc_url)
    if not gdc_html.ok:
        print(error.format("Could not connect to {}".format(gdc_url)))
        return '', ''

    gdc_soup = BeautifulSoup(gdc_html.text, 'html.parser')
    today = date.today().strftime('%B %-d')

    event_date = gdc_soup.find('div', class_='date')
    game_jam = ''
    if today in event_date.text:
        game_jam = "Game Jam {}\n{}\n".format(event_date.text.strip(), gdc_url)

    return game_jam, ''


@events
def robotics_events():
    """Robotics Club events posted to ???"""
    #TODO: 2017-03-23: No website for events.
'''
