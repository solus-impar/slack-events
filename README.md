# slack-events
[![Build Status][badge-build]](https://travis-ci.org/solus-impar/slack-events)

A python3 slack events bot.

## Installation

```
pip3 install git+https://github.com/solus-impar/slack-events.git@master
```

If you are not in a [virtualenv] you may need to use `pip3` with `sudo` or
`--user`.

## Usage
Once `slack-events` is installed you can run it from the command line. Keep in
mind that `slack-events` depends on the following environment variables:
* `SLACK_EVENTS_TOKEN`: A custom bot Slack token.
* `SLACK_EVENTS_CHANNEL`: The name of the channel to post events to.

## Schedule
If you want `slack-events` to run regularly you can add it to your `crontab` or
`launchd`.

`slack-events` will post today's events listed on these sites:
* [WWU Dept. of Computer Science](//cse.wwu.edu/computer-science)

## New Events
Is `slack-events` currently supports? Follow the
[contribution guidelines] to add one!

## Resources
Slack API: [api.slack.com](//api.slack.com/)

`slack-events` forked from
[`slack-topics`](//github.com/solus-impar/slack-topics) at commit
[`6d7719f`](//github.com/solus-impar/slack-topics/commit/6d7719ff1245d1672ce9c14c8d245865ec98e4ed).

You should also check out [wb2k].

[badge-build]: https://travis-ci.org/solus-impar/slack-events.svg?branch=master
[wb2k]: //github.com/reillysiemens/wb2k/
[virtualenv]: //virtualenv.pypa.io/en/stable/
[contribution guidelines]: //github.com/solus-impar/slack-events/blob/master/CONTRIBUTING.md
