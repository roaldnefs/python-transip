.. _quickstart:

Quickstart
==========

This page gives a introduction in how to get started with **python-transip**.

First, make sure that:

* python-transip is :ref:`installed <install>`

Below you'll find some simple example to get started.

Authentication
--------------

In order to make requests to the TransIP API we need to authenticate yourself
using an access token. To get an access token, you should first login to the
TransIP control panel. You can then generate a new token which will only be
valid for limited time.

TransIP also provide a **demo token** to authenticate yourself as the TransIP
demo user in test mode::

    eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImN3MiFSbDU2eDNoUnkjelM4YmdOIn0.eyJpc3MiOiJhcGkudHJhbnNpcC5ubCIsImF1ZCI6ImFwaS50cmFuc2lwLm5sIiwianRpIjoiY3cyIVJsNTZ4M2hSeSN6UzhiZ04iLCJpYXQiOjE1ODIyMDE1NTAsIm5iZiI6MTU4MjIwMTU1MCwiZXhwIjoyMTE4NzQ1NTUwLCJjaWQiOiI2MDQ0OSIsInJvIjpmYWxzZSwiZ2siOmZhbHNlLCJrdiI6dHJ1ZX0.fYBWV4O5WPXxGuWG-vcrFWqmRHBm9yp0PHiYh_oAWxWxCaZX2Rf6WJfc13AxEeZ67-lY0TA2kSaOCp0PggBb_MGj73t4cH8gdwDJzANVxkiPL1Saqiw2NgZ3IHASJnisUWNnZp8HnrhLLe5ficvb1D9WOUOItmFC2ZgfGObNhlL2y-AMNLT4X7oNgrNTGm-mespo0jD_qH9dK5_evSzS3K8o03gu6p19jxfsnIh8TIVRvNdluYC2wo4qDl5EW5BEZ8OSuJ121ncOT1oRpzXB0cVZ9e5_UVAEr9X3f26_Eomg52-PjrgcRJ_jPIUYbrlo06KjjX2h0fzMr21ZE023Gw

API Client
----------

Initializing a new TransIP API client with python-transip is very simple.

Begin by importing the module::

    >>> import transip

Now, lets initialize a :class:`TransIP <transip.TransIP>` object called
``client``. We need to provide it with our TransIP access token in order to
authenticate the requests to the TransIP API. The example below uses the **demo
token** to authenticate as the TransIP demo user in test mode::

    >>> client = transip.TransIP(access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImN3MiFSbDU2eDNoUnkjelM4YmdOIn0.eyJpc3MiOiJhcGkudHJhbnNpcC5ubCIsImF1ZCI6ImFwaS50cmFuc2lwLm5sIiwianRpIjoiY3cyIVJsNTZ4M2hSeSN6UzhiZ04iLCJpYXQiOjE1ODIyMDE1NTAsIm5iZiI6MTU4MjIwMTU1MCwiZXhwIjoyMTE4NzQ1NTUwLCJjaWQiOiI2MDQ0OSIsInJvIjpmYWxzZSwiZ2siOmZhbHNlLCJrdiI6dHJ1ZX0.fYBWV4O5WPXxGuWG-vcrFWqmRHBm9yp0PHiYh_oAWxWxCaZX2Rf6WJfc13AxEeZ67-lY0TA2kSaOCp0PggBb_MGj73t4cH8gdwDJzANVxkiPL1Saqiw2NgZ3IHASJnisUWNnZp8HnrhLLe5ficvb1D9WOUOItmFC2ZgfGObNhlL2y-AMNLT4X7oNgrNTGm-mespo0jD_qH9dK5_evSzS3K8o03gu6p19jxfsnIh8TIVRvNdluYC2wo4qDl5EW5BEZ8OSuJ121ncOT1oRpzXB0cVZ9e5_UVAEr9X3f26_Eomg52-PjrgcRJ_jPIUYbrlo06KjjX2h0fzMr21ZE023Gw")

Availability Zones
------------------

Using the
:class:`AvailabilityZoneService <transip.v6.services.AvailabilityZoneService>`
service we can retrieve all availability zone on TransIP if the form of an
:class:`AvailabilityZone <transip.v6.objects.AvailabilityZone>` object::

    >>> zones = client.availability_zones.list()
    >>> for zone in zones:
    ...     print(zone)
    <class 'transip.v6.objects.availability_zone.AvailabilityZone'> => {'name': 'ams0', 'country': 'nl', 'isDefault': False}
    <class 'transip.v6.objects.availability_zone.AvailabilityZone'> => {'name': 'rtm0', 'country': 'nl', 'isDefault': True}

We could for example print information about the default TransIP availability
zone::

    >>> for zone in zones:
    ...     if zone.isDefault:
    ...         print(f"{zone.name} is the default zone and is located in {zone.country}")
    rtm0 is the default zone and is located in nl

Domains
-------

Using the
:class:`DomainService <transip.v6.services.DomainService>`
service we can retrieve all domains in your TransIP account in the form of a
:class:`Domain <transip.v6.objects.Domain>` object::

    >>> domains = client.domains.list()
    >>> for domain in domains:
    ...     print(domain)
    <class 'transip.v6.objects.domain.Domain'> => {'name': 'transipdemo.be', 'authCode': '##########', 'isTransferLocked': False, 'registrationDate': '2011-04-29', 'renewalDate': '2021-04-29', 'isWhitelabel': False, 'isDnsOnly': False, 'cancellationDate': '', 'cancellationStatus': '', 'hasActionRunning': False, 'supportsLocking': True, 'tags': []}
    <class 'transip.v6.objects.domain.Domain'> => {'name': 'transipdemo.de', 'authCode': '##########', 'isTransferLocked': False, 'registrationDate': '2011-04-29', 'renewalDate': '2021-04-29', 'isWhitelabel': False, 'isDnsOnly': False, 'cancellationDate': '', 'cancellationStatus': '', 'hasActionRunning': False, 'supportsLocking': False, 'tags': []}
    <class 'transip.v6.objects.domain.Domain'> => {'name': 'transipdemo.net', 'authCode': '##########', 'isTransferLocked': True, 'registrationDate': '2011-04-29', 'renewalDate': '2021-04-29', 'isWhitelabel': False, 'isDnsOnly': False, 'cancellationDate': '', 'cancellationStatus': '', 'hasActionRunning': False, 'supportsLocking': True, 'tags': []}
    <class 'transip.v6.objects.domain.Domain'> => {'name': 'transipdemonstratie.com', 'authCode': '##########', 'isTransferLocked': True, 'registrationDate': '2011-04-29', 'renewalDate': '2021-04-29', 'isWhitelabel': False, 'isDnsOnly': False, 'cancellationDate': '', 'cancellationStatus': '', 'hasActionRunning': False, 'supportsLocking': True, 'tags': []}
    <class 'transip.v6.objects.domain.Domain'> => {'name': 'transipdemonstratie.nl', 'authCode': '##########', 'isTransferLocked': False, 'registrationDate': '2011-04-29', 'renewalDate': '2021-04-29', 'isWhitelabel': False, 'isDnsOnly': False, 'cancellationDate': '', 'cancellationStatus': '', 'hasActionRunning': False, 'supportsLocking': False, 'tags': []}

We could also retrieve a single :class:`Domain <transip.v6.objects.Domain>`
object by its name::

    >>> domain = client.domains.get('transipdemonstratie.nl')
    >>> print(f"{domain.name} was registered on {domain.registrationDate}")
    transipdemonstratie.nl was registered on 2011-04-29

We could also cancel a single :class:`Domain <transip.v6.objects.Domain>`
object by its name::

    >>> client.domains.delete('transipdemonstratie.nl')

Invoices
--------

Using the
:class:`InvoiceService <transip.v6.services.InvoiceService>`
service we can retrieve all invoices in your TransIP account in the form of a
:class:`Invoice <transip.v6.objects.Invoice>` object::

    >>> invoices = client.invoices.list()
    >>> for invoice in invoices:
    ...     print(invoice)
    <class 'transip.v6.objects.invoice.Invoice'> => {'invoiceNumber': 'F0000.1911.0000.0004', 'creationDate': '2020-01-01', 'payDate': '2020-01-01', 'dueDate': '2020-02-01', 'invoiceStatus': 'waitsforpayment', 'currency': 'EUR', 'totalAmount': 1000, 'totalAmountInclVat': 1240}

We could also retrieve a single :class:`Invoice <transip.v6.objects.Invoice>`
object by its invoice number::

    >>> invoice = client.invoices.get('F0000.1911.0000.0004')
    >>> print(f"{invoice.invoiceNumber} has status '{invoice.invoiceStatus}'")
    F0000.1911.0000.0004 has status 'waitsforpayment'

VPSs
----

Using the
:class:`VpsService <transip.v6.services.VpsService>`
service we can retrieve all VPSs in your TransIP account in the form of a
:class:`Vps <transip.v6.objects.Vps>` object::

    >>> vpss = client.vpss.list()
    >>> for vps in vpss:
    ...     print(vps)
    <class 'transip.v6.objects.vps.Vps'> => {'name': 'transipdemo-vps', 'description': '', 'productName': 'vps-bladevps-x1', 'operatingSystem': 'FreeBSD 10.0-RELEASE', 'diskSize': 52428800, 'memorySize': 1048576, 'cpus': 3, 'status': 'running', 'ipAddress': '141.138.136.129', 'macAddress': '52:54:00:19:a7:20', 'currentSnapshots': 1, 'maxSnapshots': 1, 'isLocked': False, 'isBlocked': False, 'isCustomerLocked': False, 'availabilityZone': 'ams0', 'tags': ['customTag', 'anotherTag']}
    <class 'transip.v6.objects.vps.Vps'> => {'name': 'transipdemo-vps2', 'description': '', 'productName': 'vps-bladevps-x1', 'operatingSystem': 'Debian 7', 'diskSize': 52428800, 'memorySize': 1048576, 'cpus': 1, 'status': 'stopped', 'ipAddress': '149.210.192.184', 'macAddress': '52:54:00:51:39:ff', 'currentSnapshots': 0, 'maxSnapshots': 0, 'isLocked': False, 'isBlocked': False, 'isCustomerLocked': False, 'availabilityZone': 'ams0', 'tags': []}
    <class 'transip.v6.objects.vps.Vps'> => {'name': 'transipdemo-vps3', 'description': '', 'productName': 'vps-bladevps-x1', 'operatingSystem': 'Debian 7', 'diskSize': 52428800, 'memorySize': 1048576, 'cpus': 2, 'status': 'running', 'ipAddress': '149.210.192.185', 'macAddress': '52:54:00:d2:6a:9f', 'currentSnapshots': 1, 'maxSnapshots': 1, 'isLocked': False, 'isBlocked': False, 'isCustomerLocked': True, 'availabilityZone': 'ams0', 'tags': []}
    <class 'transip.v6.objects.vps.Vps'> => {'name': 'transipdemo-vps4', 'description': '', 'productName': 'vps-bladevps-x1', 'operatingSystem': 'Ubuntu 14.04 LTS', 'diskSize': 52428800, 'memorySize': 1048576, 'cpus': 1, 'status': 'running', 'ipAddress': '149.210.192.186', 'macAddress': '52:54:00:db:27:25', 'currentSnapshots': 0, 'maxSnapshots': 3, 'isLocked': False, 'isBlocked': False, 'isCustomerLocked': False, 'availabilityZone': 'ams0', 'tags': []}
    <class 'transip.v6.objects.vps.Vps'> => {'name': 'transipdemo-vps5', 'description': '', 'productName': 'vps-bladevps-x4', 'operatingSystem': 'DirectAdmin 1.45.0 + CentOS 6.5', 'diskSize': 157286400, 'memorySize': 4194304, 'cpus': 2, 'status': 'running', 'ipAddress': '149.210.192.187', 'macAddress': '52:54:00:0c:0d:f3', 'currentSnapshots': 0, 'maxSnapshots': 1, 'isLocked': False, 'isBlocked': False, 'isCustomerLocked': False, 'availabilityZone': 'ams0', 'tags': []}
    <class 'transip.v6.objects.vps.Vps'> => {'name': 'transipdemo-vps6', 'description': '', 'productName': 'vps-bladevps-pro-x32', 'operatingSystem': 'Plesk Onyx Web Pro Edition 17.8.11 + CentOS 7', 'diskSize': 1048576000, 'memorySize': 33554432, 'cpus': 6, 'status': 'running', 'ipAddress': '149.210.192.188', 'macAddress': '52:54:00:7a:96:03', 'currentSnapshots': 0, 'maxSnapshots': 1, 'isLocked': False, 'isBlocked': False, 'isCustomerLocked': False, 'availabilityZone': 'ams0', 'tags': []}

We could also retrieve a single :class:`Vps <transip.v6.objects.Vps>`
object by its name::

    >>> vps = client.vpss.get('transipdemo-vps')
    >>> print(f"{vps.name} runs {vps.operatingSystem} and has IP address: '{vps.ipAddress}'")
    transipdemo-vps runs FreeBSD 10.0-RELEASE and has IP address: '141.138.136.129'

We could also cancel a single :class:`Vps <transip.v6.objects.Vps>`
object by its name::

    >>> client.vpss.delete('transipdemo-vps')

Errors and Exceptions
---------------------

In the event of a API problem (e.g. authentication error, requested resource not
found, etc.) python-transip will raise a :exc:`~transip.exceptions.TransIPHTTPError`
exception.

All exceptions that python-transip explicitly raises inherit from
:exc:`~transip.exceptions.TransIPError`.
