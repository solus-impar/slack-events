import os
import sys
import random

import wikipedia

from topics.utils import fetch_json


def topic_man_page():
    """Randomly select a man page from /usr/share/man/."""
    sec = random.randrange(1, 9)
    man_dir = "/usr/share/man/man{}/".format(sec)
    man_url = "http://man7.org/linux/man-pages/man{}/".format(sec)

    try:
        page = random.choice(os.listdir(man_dir))
    except IndexError:
        sys.exit("tb2k: error: no man pages in section {}".format(sec))
    except FileNotFoundError:
        sys.exit("tb2k: error: {} does not exist".format(man_dir))
    except PermissionError:
        sys.exit("tb2k: error: {}: permission denied".format(man_dir))

    man_url = "{}{}.{}.html".format(man_url, page.split('.')[0], sec)
    return "{}({})".format(page.split('.')[0], sec), man_url


def topic_wikipedia_programming_language():
    """Randomly select a programming language from Wikipedia."""
    title = 'List of programming languages'
    page = wikipedia.page(title=title)
    lang = random.choice(page.links)
    lang_url = "https://en.wikipedia.org/wiki/{}".format(lang.replace(' ','_'))
    return lang, lang_url


def topic_top_hacker_news_story():
    """Select the current top Hacker News story."""
    hn_api = 'https://hacker-news.firebaseio.com/v0'

    stories_url = "{}/topstories.json".format(hn_api)
    stories = fetch_json(stories_url)

    story_url = "{}/item/{}.json".format(hn_api, stories[0])
    story = fetch_json(story_url)

    return story['title'], story['url']