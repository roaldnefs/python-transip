.. python-transip documentation master file, created by
   sphinx-quickstart on Tue Dec 29 09:14:35 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://github.com/roaldnefs/python-transip/blob/main/logo.png?raw=true
    :target: https://github.com/roaldnefs/python-transip

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://img.shields.io/pypi/pyversions/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge
    :target: https://pypi.org/project/python-transip/
.. image:: https://img.shields.io/pypi/dm/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge
    :target: https://pypi.org/project/python-transip/
.. image:: https://img.shields.io/pypi/format/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge
    :target: https://pypi.org/project/python-transip/
.. image:: https://img.shields.io/github/license/roaldnefs/python-transip?color=187dc1&style=for-the-badge
    :target: https://raw.githubusercontent.com/roaldnefs/python-transip/main/COPYING
.. image:: https://img.shields.io/github/workflow/status/roaldnefs/python-transip/tests?color=187dc1&label=CI&logo=github&style=for-the-badge
    :target: https://github.com/roaldnefs/python-transip/actions
.. image:: https://img.shields.io/github/contributors/roaldnefs/python-transip?color=187dc1&logo=github&style=for-the-badge
    :target: https://github.com/roaldnefs/python-transip/graphs/contributors

**python-transip** is an Python wrapper for the TransIP REST API.

-------------------

**Example usage**::

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

**python-transip** allows you to create, read and update resources on TransIP
with ease. 

The User Guide
--------------

.. toctree::
   :maxdepth: 2

   user/install
   user/quickstart
