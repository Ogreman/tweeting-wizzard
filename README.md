# tweeting-wizzard

Installation
------------

Recommend using virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

    $ git clone git@github.com:Ogreman/tweeting-wizzard.git
    $ cd tweeting-wizzard
    $ pip install .
    $ export CONSUMER_KEY="MY_TWITTER_CONSUMER_KEY"
    $ export CONSUMER_SECRET="MY_TWITTER_CONSUMER_SECRET"
    $ export ACCESS_TOKEN="MY_TWITTER_ACCESS_TOKEN"
    $ export ACCESS_SECRET="MY_TWITTER_ACCESS_SECRET"

See here for retrieval of your Twitter API keys: https://apps.twitter.com/

Usage
-----

    $ wizzard tweet [message]
    
  Example:
  
    $ wizzard tweet I am not a werewolf.
    Sent.
    

Other Uses
----------

    Usage: wizzard [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --verbose
      --debug
      --silent
      --help     Show this message and exit.
    
    Commands:
      delete
      last
      stream
      tweet


Environment Variables & Virtual Environments
--------------------------------------------

With virtualenvwrapper installed, it is recommended to add the following to the activation hooks:

    $ mkvirtualenv wizzard-env
    $ cd $VIRTUAL_ENV/bin
    $ echo export CONSUMER_KEY="MY_TWITTER_CONSUMER_KEY" >> postactivate
    $ echo export CONSUMER_SECRET="MY_TWITTER_CONSUMER_SECRET" >> postactivate
    $ echo export ACCESS_TOKEN="MY_TWITTER_ACCESS_TOKEN" >> postactivate
    $ echo export ACCESS_SECRET="MY_TWITTER_ACCESS_SECRET" >> postactivate
    $ echo unset CONSUMER_KEY >> postdeactivate
    $ echo unset CONSUMER_SECRET >> postdeactivate
    $ echo unset ACCESS_TOKEN >> postdeactivate
    $ echo unset ACCESS_SECRET >> postdeactivate
    $ deactivate
    $ workon wizzard-env
    $ echo $CONSUMER_KEY
    CONSUMER_KEY
