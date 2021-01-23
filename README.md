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
        - [The **Invoice** class](#the-invoice-class)
        - [The **InvoiceItem** class](#the-invoiceitem-class)
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
The [general TransIP API](https://api.transip.nl/rest/docs.html#general) resources allow you to manage products, availability zones and call the API test resource.
### Products
Manage available TransIP products and product specifications.
#### List all products
Retrieve al list of products with, there name, description and price.

```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# List all available TransIP products.
products = client.products.list()
# Show product information on the screen.
for product in products:
    print((
        f"Product {product.name} ({product.description}) costs "
        f"{product.price} (cents), after which it costs "
        f"{product.recurringPrice} (cents)"
    ))
```

#### List specifications for product
Get the specification for a product. This will list all the different elements for a product with the amount that it comes with, e.g. a a `vps-bladevps-x4` has 2 CPU-core elements.

```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# Show product specification information on the screen for all available
# TransIP products.
for product in client.products.list():
    print(f"Product {product.name} ({product.description}):")
    elements = product.elements.list()
    for element in elements:
        print(f"- Has {element.amount} {element.name}: {element.description}")
```

### Availability Zones
Manage TransIP availability zones.
#### List availability zones
Retrieve the available availability zones:
```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# List all available availability zones.
zones = client.availability_zones.list()
# Show availability zone information on the screen.
for zone in zones:
    print((
        f"Availability zone {zone.name} in {zone.country} "
        f"(default: {zone.isDefault})"
    ))
```

### API Test
A simple test resource to make sure everything is working.

```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# Check if everything is working by calling the API test resource.
if client.api_test.test():
    print("Everthing is working!")
```

## Account
The [account TransIP API](https://api.transip.nl/rest/docs.html#account) resources allow you to manage invoices and SSH keys.

### Invoices
Manage invoices attached to your TransIP account.

### The **Invoice** class
When listing all invoices attached to your TransIP account, a list of **transip.v6.objects.Invoice** objects is returned.

**_class_ Invoice**

The **Invoice** class makes the following attributes available:

- **invoiceNumber**: The invoice number.
- **creationDate**: The invoice creation date.
- **payDate**: The invoice paid date.
- **dueDate**: The invoice deadline.
- **invoiceStatus**: The invoice status.
- **currency**: The currency used for this invoice.
- **totalAmount**: The invoice total (_displayed in cents_).
- **totalAmountInclVat**: The invoice total including VAT (_displayed in cents_).
- **items**: The service to list detailed information on the individual invoice items.


### The **InvoiceItem** class
When listing all invoices items attached to a **transip.v6.objects.Invoice** object, a list of **transip.v6.objects.InvoiceItem** objects is returned.

**_class_ InvoiceItem**

The **InvoiceItem** class makes the following attributes available:

- **product**: The product name.
- **description**: The product description.
- **isRecurring**: Whether or not the payment is recurring.
- **date**: The date when the order line item was up for invoicing.
- **quantity**: The quantity of the invoice item.
- **price**: The price excluding VAT (_displayed in cents_).
- **priceInclVat**: The price including VAT (_displayed in cents_).
- **vat**: The amount of VAT charged.
- **vatPercentage**: The percentage used to calculate the VAT.
- **discounts**: The dictionary containing the applied discounts.
    - **description**: The applied discount description.
    - **amount**: The discounted amount (_in cents_).

The class has the following methods:

- **pdf(_file_path_)** stores the invoice as a PDF file on a location provided by the **file_path** keyword argument. When the **file_path** is a directory, the PDF file will be saved using the invoice number as its basename.

#### List all invoices
Retrieve all invoices attached to your TransIP account by calling **transip.TransIP.invoices.list()**. This will return a list of **transip.v6.objects.Invoice** objects.

For example:
```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# List all invoices attached to your TransIP account.
invoices = client.invoices.list()
# Show invoice information on the screen.
for invoice in invoices:
    print(f"Invoice {invoice.invoiceNumber} was paid on {invoice.payDate}")
```

**Note:** when using the demo access token, the API currently doesn't list any invoices.

#### List a single invoice
Retrieve a single invoice attached to your TransIP account by its invoice number by calling **transip.TransIP.invoices.get(_id_)**. This will return a **transip.v6.objects.Invoice** object.

For example:
```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# Retrieve a single invoice by its invoice number.
invoice = client.invoices.get('F0000.1911.0000.0004')
# Show invoice information on the screen.
print(f"Invoice {invoice.invoiceNumber} was paid on {invoice.payDate}")
```

**Note:** when using the demo access token, the API currently doesn't list any invoices.

#### List invoice items by invoice number
Retrieve the invoice items of a single invoice attached to your TransIP account by its invoice number by calling **items.list()** on a **transip.v6.objects.Invoice** object. This will return a list of **transip.v6.objects.InvoiceItem** objects.

For example:
```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# Retrieve a single invoice by its invoice number.
invoice = client.invoices.get('F0000.1911.0000.0004')
# Retrieve all items of a single invoice.
items = invoice.items.list()
# Show invoice information on the screen.
for item in items:
    print(f"Product {item.product} ({item.description})")
```

**Note:** when using the demo access token, the API currently doesn't list any invoices.

#### Retrieve an invoice as PDF file
Any of the invoices can be saved as a PDF file by calling **pdf(_file_path_)** on a **transip.v6.objects.Invoice** object:

```python
import transip
# Initialize a client using the TransIP demo token.
client = transip.TransIP(access_token=transip.v6.DEMO_TOKEN)

# Retrieve a single invoice by its invoice number.
invoice = client.invoices.get('F0000.1911.0000.0004')
# Save the invoice as a PDF file.
invoice.pdf('/path/to/invoices/')
```

**Note:** when using the demo access token, the API currently doesn't list any invoices.

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


