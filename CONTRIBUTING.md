# Contributing to slack-events

`slack-events` keeps plugins in the [`events.callables`][events callables] module. If
you'd like to contribute an event source of your own you can submit a pull
request to this repository adding a callable object to that module. Events
callables **MUST** conform to the following specification:

1. Be decorated with the `@events` decorator from [`events.utils`][events utils].
2. Take no arguments.
3. Return an `events` string and a `channel` string as a tuple.
  - `events` and `channel` _can_ be the empty string.
  - If `channel` is an empty string, then it deaults to `SLACK_EVENTS_CHANNEL` if set
  or `general`.

An example event function might look like this:
```python
@events
def wwucs_table_tennis_tournament():
    event = 'Table Tennis Tournament in CF405 @ 5PM!'
    channel = 'pingpong'
    return event, channel
```

An example events class might look like this:
```python
@events
class WwucsTableTenisTournament:
    def __init__(self):
        self.event = 'Table Tennis Toun!'
        self.message = 'https://wwucs.slack.com'
        self.channel = 'wwu'

    def __call__(self):
        return self.event, self.message, self.channel
```

## Note
The `@event` decorator sets a special attribute, `__event__`, on the event
function to signal that it is a event, but also for naming purposes. The
`__event__` attribute is used to provide source for links. For example,
the above function would show up in a Slack message like
> WWU CS Rules: https://wwucs.slack.com

and the above class would show up like
> Western Washington University Computer Science Rules: https://wwucs.slack.com

Therefore, it behooves contributors to pick descriptive names for new event
callables.

[event callables]: https://github.com/solus-impar/slack-events/blob/master/events/callables.py
[event utils]: https://github.com/solus-impar/slack-events/blob/master/events/utils.py
