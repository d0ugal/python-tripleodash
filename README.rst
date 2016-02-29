TripleO Dashboard
=================

This is a terminal Dashboard for TripleO. It aims to provide an overview of
the deployment by showing you the images, nodes and Heat stack all together.
This helps you see your progress when deploying and will also help when
troubleshooting.

.. image:: https://img.shields.io/pypi/v/python-tripleodash.svg
        :target: https://pypi.python.org/pypi/python-tripleodash

.. image:: https://img.shields.io/pypi/dm/python-tripleodash.svg
        :target: https://pypi.python.org/pypi/python-tripleodash

.. image:: https://travis-ci.org/d0ugal/python-tripleodash.png?branch=master
        :target: https://travis-ci.org/d0ugal/python-tripleodash

.. image:: https://readthedocs.org/projects/python-tripleodash/badge/?version=latest
        :target: https://readthedocs.org/projects/python-tripleodash/?badge=latest
        :alt: Documentation Status

Usage
-----

You can either install tripleodash system wide.

.. code-block:: shell

    $ source ~/stackrc
    $ pip install python-tripleodash
    $ tripleodash


Or, run it in a virtualenv with Tox. This may be favourable if you want to
run tripleodash without touching the system Python install.

.. code-block:: shell

    $ source ~/stackrc
    $ git clone https://github.com/d0ugal/python-tripleodash.git
    $ cd python-tripleodash
    $ tox -e venv -- tripleodash

.. note::

   If you don't have a pip and tox package for your system, install pip with
   get-pip.py_ and then :code:`sudo pip install tox`

.. _get-pip.py: https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py


`Further documentation and screenshots <http://python-tripleodash.rtfd.org/>`_.

