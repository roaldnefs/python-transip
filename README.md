# Python TransIP

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/python-transip/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/python-transip/)
[![PyPI - Format](https://img.shields.io/pypi/format/python-transip?color=187dc1&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/python-transip/)
[![License](https://img.shields.io/github/license/roaldnefs/python-transip?color=187dc1&style=for-the-badge)](https://raw.githubusercontent.com/roaldnefs/python-transip/main/COPYING.LESSER)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/roaldnefs/python-transip/tests?color=187dc1&label=CI&logo=github&style=for-the-badge)](https://github.com/roaldnefs/python-transip/actions)
[![GitHub contributors](https://img.shields.io/github/contributors/roaldnefs/python-transip?color=187dc1&logo=github&style=for-the-badge)](https://github.com/roaldnefs/python-transip/graphs/contributors)

**python-transip** is an Python wrapper for the **TransIP REST API V6**.

- [Introduction](#introduction)
    - [Installation](#installation)
    - [Documentation](#documentation)
    - [Authentication](#authentication)
- [General](#general)
    - [Products](#products)
        - [List all products](#list-all-products)
        - [List specifications for product](#list-specifications-for-product)
    - [Availability Zones](#availability-zones)
        - [List availability zones](#list-availability-zones)
    - [API Test](#api-test)
- [Account](#account)
    - [Invoices](#invoices)
        - [List all invoices](#list-all-invoices)
        - [List a single invoice](#list-a-single-invoice)
        - [List invoice items by invoice number](#list-invoice-items-by-invoice-number)
        - [Retrieve an invoice as PDF file](#retrieve-an-invoice-as-PDF-file)
    - [SSH Keys](#ssh-keys)
        - [List all SSH keys](#list-all-ssh-keys)
        - [Get SSH key by id](#get-ssh-key-by-id)
        - [Add a new SSH key](#add-a-new-ssh-key)
        - [Update an SSH key](#update-an-ssh-key)
        - [Delete an SSH key](#delete-an-ssh-key)
- [Domains](#domains)
- [VPS](#vps)
- [HA-IP](#ha-ip)
- [Colocation](#colocation)

## Introduction

Welcome to the Python TransIP documentation.

**REST API V6**

**python-transip** implements the new TransIP REST API to manage all products in a RESTful way, this means that for most products you can make simple create, update and delete calls.

The wrapper tries to stay close to the naming convention of the official [API documentation](https://api.transip.nl/rest/docs.html).

**SOAP V5 API (deprecated)**

Users are strongly advised to use the new REST API because the SOAP API has been deprecated. If you still depend on functionality that has not yet been implemented in **python-transip** consider raising a [feature request](https://github.com/roaldnefs/python-transip/issues/new/choose) and using [transip-api (_deprecated_)](https://github.com/benkonrath/transip-api) in the meanwhile.

### Installation

**python-transip** is available on PyPI:

```console
$ python -m pip install python-transip
```

**python-transip** officially supports Python 3.6+.

### Documentation

The full API Reference and User Guide is available on [Read the Docs](https://python-transip.readthedocs.io/).

### Authentication

In order to manage TransIP products via **python-transip** you will need to be authenticated. The **REST API V6** requires an access token that makes use of the [JSON Web Token](https://jwt.io/) standard.

To get an access token, you should first generate a key pair using the [control panel](https://www.transip.nl/cp/account/api). You can than pass the private key to the **python-transip** client to allow the client to generate a new access token, e.g.:

```python
import transip

# You can initialize a TransIP client using a private key directly.
PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
...
'''
client = transip.TransIP(login='demouser', private_key=PRIVATE_KEY)

# You can also initialize a TransIP client by telling it where to find the
# private key file on the system.
client = transip.TransIP(login='demouser', private_key_file='/path/to/private.key')
```

Alternatively you can also authenticate by providing an access token. This is especially useful when testing the API with the [demo token](https://api.transip.nl/rest/docs.html#header-demo-token), e.g.:

```python
import transip

# You can initialize a TransIP client using an access token directly.
DEMO_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImN3MiFSbDU2eDNoUnkjelM4YmdOIn0.eyJpc3MiOiJhcGkudHJhbnNpcC5ubCIsImF1ZCI6ImFwaS50cmFuc2lwLm5sIiwianRpIjoiY3cyIVJsNTZ4M2hSeSN6UzhiZ04iLCJpYXQiOjE1ODIyMDE1NTAsIm5iZiI6MTU4MjIwMTU1MCwiZXhwIjoyMTE4NzQ1NTUwLCJjaWQiOiI2MDQ0OSIsInJvIjpmYWxzZSwiZ2siOmZhbHNlLCJrdiI6dHJ1ZX0.fYBWV4O5WPXxGuWG-vcrFWqmRHBm9yp0PHiYh_oAWxWxCaZX2Rf6WJfc13AxEeZ67-lY0TA2kSaOCp0PggBb_MGj73t4cH8gdwDJzANVxkiPL1Saqiw2NgZ3IHASJnisUWNnZp8HnrhLLe5ficvb1D9WOUOItmFC2ZgfGObNhlL2y-AMNLT4X7oNgrNTGm-mespo0jD_qH9dK5_evSzS3K8o03gu6p19jxfsnIh8TIVRvNdluYC2wo4qDl5EW5BEZ8OSuJ121ncOT1oRpzXB0cVZ9e5_UVAEr9X3f26_Eomg52-PjrgcRJ_jPIUYbrlo06KjjX2h0fzMr21ZE023Gw"
client = transip.TransIP(access_token=DEMO_TOKEN)
```

## General

### Products

#### List all products
Retrieve al list of products with, there name, description and price.

#### List specifications for product

### Availability Zones
#### List availability zones

### API Test

A simple test resource to make sure everything is working.

## Account

### Invoices

#### List all invoices
#### List a single invoice
#### List invoice items by invoice number
#### Retrieve an invoice as PDF file

### SSH Keys
#### List all SSH keys
#### Get SSH key by id
#### Add a new SSH key
#### Update an SSH key
#### Delete an SSH key

## Domains

## VPS

## HA-IP

## Colocation
