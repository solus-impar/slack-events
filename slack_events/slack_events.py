"""slack-events: A python3 slack event bot."""
import datetime
import os
import sys
from bs4 import BeautifulSoup
import requests
from slackclient import SlackClient
import slack_events.events.callables as ec


def find_id(channel, bot):
    """Find the ID of a channel and whether it is public or private.

    Args:
        channel (string): Name of channel, i.e. `general`.
        bot (SlackClient): Slack-bot for API calls.

    Returns:
        channel_id, channel_type (tuple of strings): `channel_id` for API
            calls when you can't use just `channel`. `channel_type` can be
            'channel' or 'group'.

    Raises:
        None
    """

    channels_list = bot.api_call("channels.list").get('channels')
    groups_list = bot.api_call("groups.list").get('groups')
    error = "slack-events: error: {}"

    if not channels_list and not groups_list:
        sys.exit(error.format(
            'couldn\'t enumerage channels/groups'
        ))

    # There is probably a better way to do this.
    channel_ids = [c['id'] for c in channels_list if c['name'] == channel]

    if channel_ids:
        return channel_ids[0], 'channel'

    group_ids = [g['id'] for g in groups_list if g['name'] == channel]

    if group_ids:
        return group_ids[0], 'group'
    else:
        sys.exit(error.format(
            "couldn't find #{}".format(channel)
        ))


def main():
    """Post today's events listed these sites:
        - cse.wwu.edu/computer-science

    Args:
        None

    Returns:
        None

    Raises:
        ConnectionError
    """

    token = os.environ.get('SLACK_EVENTS_TOKEN')
    channel = os.environ.get('SLACK_EVENTS_CHANNEL') or 'general'
    error = "slack-events: error: {}"

    if not token:
        sys.exit(error.format(
            'SLACK_EVENTS_TOKEN environment variable is not set'
        ))

    bot = SlackClient(token)
    if bot.rtm_connect():

        # Get all attributes in the events.functions module that are callable
        # and possess the custom __events__ attribute.
        events_callables = []
        for attr in (getattr(ec, a) for a in dir(ec)):
            if callable(attr) and hasattr(attr, '__events__'):
                events_callables.append(attr)
        for events_callable in events_callables:
            events, events_channel = events_callable()
            if events_channel:
                channel = events_channel

            channel_id, channel_type = find_id(channel, bot)

            if events:
                # Try to post events in channel.
                try:
                    source = "{}:\n{}".format(events_callable.__events__, events)
                    response = bot.api_call(
                        "chat.postMessage",
                        token=token,
                        channel=channel_id,
                        text=source,
                        as_user=True
                    )
                    if not response['ok']:
                        sys.exit(error.format(
                            "failed to post link in #{}".format(channel)
                        ))
                except requests.ConnectionError:
                    sys.exit(error.format(
                        "failed to connect to {}.".format(events)
                    ))

if __name__ == "__main__":
    main()
