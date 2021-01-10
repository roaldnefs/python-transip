[![python-transip](https://github.com/roaldnefs/python-transip/blob/main/logo.png?raw=true)](https://github.com/roaldnefs/python-transip)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/python-transip/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/python-transip/)
[![PyPI - Format](https://img.shields.io/pypi/format/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/python-transip/)
[![License](https://img.shields.io/github/license/roaldnefs/python-transip?color=187dc1&style=for-the-badge)](https://raw.githubusercontent.com/roaldnefs/python-transip/main/COPYING.LESSER)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/roaldnefs/python-transip/tests?color=187dc1&label=CI&logo=github&style=for-the-badge)](https://github.com/roaldnefs/python-transip/actions)
[![GitHub contributors](https://img.shields.io/github/contributors/roaldnefs/python-transip?color=187dc1&logo=github&style=for-the-badge)](https://github.com/roaldnefs/python-transip/graphs/contributors)

**python-transip** is an Python wrapper for the TransIP REST API.

```python
>>> import transip
# Initialize a TransIP API client
>>> client = transip.TransIP(
...     login="demouser",
...     private_key_file="/path/to/private.key"
... )
# Retrieve a list of VPSs
>>> for vps in client.vpss.list():
...     print(vps)
<class 'transip.v6.objects.Vps'> => {'name': 'transipdemo-vps', 'productName': 'vps-bladevps-x1', ... }
# Retrieve a domain and list its DNS-records
>>> domain = client.domains.get('transipdemo.net')
>>> for entry in domain.dns.list():
...     print(entry)
<class 'transip.v6.objects.DnsEntry'> => {'name': '*', 'expire': 300, 'type': 'A', 'content': '95.170.70.223'}
<class 'transip.v6.objects.DnsEntry'> => {'name': '@', 'expire': 300, 'type': 'A', 'content': '95.170.70.223'}
# Add a new DNS-record
>>> domain.dns.create({'name': '@', 'expire': 300, 'type': 'TXT', 'content': 'Python'})
```

## Installing python-transip and Supported Versions

**python-transip** is available on PyPI:

```console
$ python -m pip install python-transip
```

**python-transip** officially supports Python 3.6+.

## Documentation

API Reference and User Guide available on [Read the Docs](https://python-transip.readthedocs.io/).
