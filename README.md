# Flats

This app parse some real estates website to notify a user by e-mail when new ads are availables.

## Setup

- Set `FLAT_CONF` environment variable to your configuration file
- Install python requirements:

```shell
$ pip install -r requirements.txt
```

- Install [geckodriver](https://selenium-python.readthedocs.io/installation.html#drivers)

- Setup your configured sources:

```shell
$ python flat/commands/setup.py
```

- Scrape your ads:

```shell
$ python flat/commands/scrape.py
```