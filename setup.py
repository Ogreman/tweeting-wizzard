from setuptools import setup

setup(
    name="wizzard",
    version='1.0',
    py_modules=['wizzard'],
    install_requires=[
        'Click',
        'requests',
        'tweepy'
    ],
    entry_points='''
        [console_scripts]
        wizzard=wizzard:cli
    ''',
)

