import os
import sys
import random
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
        ValueError
    """

    channels_list = bot.api_call("channels.list").get('channels')
    groups_list = bot.api_call("groups.list").get('groups')

    assert channels_list
    assert groups_list

    # There is probably a better way to do this.
    channel_ids = [c['id'] for c in channels_list if c['name'] == channel]

    if channel_ids:
        return channel_ids[0], 'channel'

    group_ids = [g['id'] for g in groups_list if g['name'] == channel]

    if group_ids:
        return group_ids[0], 'group'
    else:
        raise ValueError


def test_slack_bot():
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

    assert token

    bot = SlackClient(token)
    if bot.rtm_connect():

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
                    assert response['ok']

                except:
                    raise requests.ConnectionError

if __name__ == "__main__":
    main()
