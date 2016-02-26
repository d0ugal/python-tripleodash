Welcome to the TripleO Dashboard Docs
=====================================

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


Screenshots
-----------

A fresh undercloud
~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-01-fresh-undercloud.png
    :width: 100%


After uploading images
~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-02-images-uploaded.png
    :width: 100%


Registering baremetal nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-03-nodes-registered.png
    :width: 100%


Viewing a table of the nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-04-view-nodes.png
    :width: 100%


Introspecting the nodes
~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-05-introspection.png
    :width: 100%


Viewing a table of the nodes during introspection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-06-introspection-node-list.png
    :width: 100%


Starting a deploy
~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-07-stack-create.png
    :width: 100%


The progress of a deploy
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-08-nodes-becoming-active.png
    :width: 100%


Seeing instances being assigned in the node list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-09-node-instances.png
    :width: 100%


After a deploy is finished
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-10-stack-create-complete.png
    :width: 100%


Updating a deployment
~~~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-11-stack-update.png
    :width: 100%


A failed deployment
~~~~~~~~~~~~~~~~~~~

.. image:: images/screenshots/screenshot-12-stack-update-failed.png
    :width: 100%
