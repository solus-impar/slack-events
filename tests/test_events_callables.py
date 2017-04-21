import events.callables as ec


def test_events_callables():
    """events.callables module: plugins for slack-events.

    Below is some of the requirements for plugins.

    Args:
        None

    Returns:
        events (str), channel (str): `events` and `channel` can be empty.

    Raises:
        Not required, but use when needed.
    """

    events_callables = []
    for attr in (getattr(ec, a) for a in dir(ec)):
        if callable(attr) and hasattr(attr, '__events__'):
            events_callables.append(attr)
    for events_callable in events_callables:
        event, channel = events_callable()
        assert isinstance(event, str)
        assert isinstance(channel, str)
