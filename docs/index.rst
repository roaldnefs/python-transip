.. python-transip documentation master file, created by
   sphinx-quickstart on Tue Dec 29 09:14:35 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-transip's documentation!
==========================================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://pepy.tech/badge/python-transip/month
    :target: https://pepy.tech/project/python-transip

.. image:: https://img.shields.io/pypi/l/python-transip.svg
    :target: https://pypi.org/project/python-transip/

.. image:: https://img.shields.io/pypi/pyversions/python-transip.svg
    :target: https://pypi.org/project/python-transip/

**python-transip** is an Python wrapper for the TransIP REST API.

-------------------

**Example usage**::

   >>> from transip import TransIP
   >>> client = TransIP(access_token="REDACTED")
   >>> domains = client.domains.list()
   >>> domain = domains[0]
   >>> domain.registrationDate
   '2011-04-29'

**python-transip** allows you to create, read and update resources on TransIP
with ease. 

The User Guide
--------------

.. toctree::
   :maxdepth: 2

   user/install
