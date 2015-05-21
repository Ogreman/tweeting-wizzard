#! /usr/bin/python

import os
import tweepy
import requests
import click

requests.packages.urllib3.disable_warnings()


CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_SECRET', None)
KEYS = (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class Config(object):

    def __init__(self):
        self.verbose = False
        self.debug = False
        self.silent = False

    @property
    def silent(self):
        return self._silent

    @silent.setter
    def silent(self, value):
        if value:
            click.echo = lambda m: None
            click.secho = lambda m, **w: None
        self._silent = value


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--silent', is_flag=True)
@pass_config
def cli(config, verbose, debug, silent): 
    if any(key is None for key in KEYS):
        raise click.ClickException('Key not set!')       
    config.verbose = verbose
    config.debug = debug
    config.silent = silent

    if debug:
        click.secho(
            'Verbose set to {0}.'
            .format(config.verbose), 
            fg="cyan"
        )
        click.secho(
            'Debug set to {0}.'
            .format(config.debug), 
            fg="cyan"
        )


@cli.command()
@click.option('--to-self', is_flag=True)
@click.argument('message', nargs=-1)
@pass_config
def tweet(config, to_self, message):
    if not message:
        raise click.ClickException('Missing message.')  
    if config.verbose:
        click.echo("Tweeting...")
    try:
        tweeter = TwitterAPI()
        tweeter.tweet(
            message=' '.join(message), 
            to_self=to_self
        )
    except tweepy.error.TweepError as e:
        if config.debug:
            click.secho(str(e), fg="red")
        click.secho("Failed!", fg="red")
    else:
        click.secho("Sent.", fg="green")
    if config.verbose:
        click.echo("Done.")


@cli.command()
@click.option('-f', '--force', is_flag=True)
@pass_config
def delete(config, force):
    if config.verbose:
        click.echo("Getting last tweet...")
    try:
        tweeter = TwitterAPI()
        if not force:
            click.secho(
                tweeter.last_tweet.text.encode('utf-8'),
                fg="yellow"
            )
            click.confirm("Delete?", abort=True)
        del tweeter.last_tweet
    except tweepy.error.TweepError as e:
        if config.debug:
            click.secho(e.reason, fg="red")
        click.secho("Failed!", fg="red")
    else:
        click.secho("Deleted.", fg="green")
    if config.verbose:
        click.echo("Done.")


class TwitterAPI(object):
    
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
 
    def tweet(self, message, to_self=False):
        if to_self:
            self.api.update_status(
                status=message, 
                in_reply_to_status_id=self.last_tweet.id
            )
        else:
            self.api.update_status(status=message)

    @property
    def last_tweet(self):
        if not hasattr(self, '_last_tweet'):
            self._last_tweet = self.get_last_tweet()
        return self._last_tweet

    @last_tweet.deleter
    def last_tweet(self):
        self.api.destroy_status(self.last_tweet.id)
        del self._last_tweet

    def get_last_tweet(self):
        return self.api.user_timeline(count=1)[0]
        