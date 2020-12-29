# python-transip

**python-transip** is an Python wrapper for the TransIP REST API.

```python
>>> from transip import TransIP
>>> client = TransIP(access_token="REDACTED")
>>> domains = client.domains.list()
>>> domain = domains[0]
>>> domain.registrationDate
'2011-04-29'
```

[![CI Tests](https://github.com/roaldnefs/python-transip/workflows/Test/badge.svg?event=push)](https://github.com/roaldnefs/python-transip/actions)
[![Downloads](https://pepy.tech/badge/python-transip/month)](https://pepy.tech/project/python-transip/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/python-transip.svg)](https://pypi.org/project/python-transip)
[![Contributors](https://img.shields.io/github/contributors/roaldnefs/python-transip.svg)](https://github.com/roaldnefs/python-transip/graphs/contributors)

## Installing python-transip and Supported Versions

**python-transip** is available on PyPI:

```console
$ python -m pip install python-transip
```

**python-transip** officially supports Python 3.6+.

## Documentation

API Reference and User Guide available on [Read the Docs](https://python-transip.readthedocs.io/).
