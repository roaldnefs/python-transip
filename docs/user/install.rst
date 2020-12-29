.. _install:

Installation of python-transip
==============================

This part of the documentation covers the installation of python-transip.
The first step to using any software package is getting it properly installed.

Using pip
---------

To install python-transip, simply run this simple command in your terminal of
choice::

    $ python -m pip install python-transip

Get the Source Code
-------------------

python-transip is actively developed on GitHub, where the code is
`available <https://github.com/roaldnefs/python-transip>`_.

You can either clone the public repository::

    $ git clone git://github.com/roaldnefs/python-transip.git

Or, download the `tarball <https://github.com/roaldnefs/python-transip/tarball/master>`_::

    $ curl -OL https://github.com/roaldnefs/python-transip/tarball/master
    # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd python-transip
    $ python -m pip install .
