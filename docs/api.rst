.. py:currentmodule:: UCube

.. _ucube_main:

UCubeClient
=============

.. autoclass:: UCube.UCubeClient
    :members:

.. _clients_main:

Clients
========

=================
UCubeClientSync
=================
.. autoclass:: UCube.UCubeClientSync
    :members:

==================
UCubeClientAsync
==================
.. autoclass:: UCube.UCubeClientAsync
    :members:

.. _obj_types:

Models
======

=========
BaseModel
=========
.. autoclass:: UCube.models.BaseModel
    :members:

====
Club
====
.. autoclass:: UCube.models.Club
    :members:

=====
Image
=====
.. autoclass:: UCube.models.Image
    :members:

.. _obj_creation:

Model Creation
==============
.. automodule:: UCube.objects
    :members:

.. _obj_exception:

Exceptions
==========

.. _invalid_token_exc:

=============
Invalid Token
=============
.. autoexception:: UCube.InvalidToken
    :members:

==================
InvalidCredentials
==================
.. autoexception:: UCube.InvalidCredentials
    :members:

====================
Something Went Wrong
====================
.. autoexception:: UCube.SomethingWentWrong
    :members:

===========
LoginFailed
===========
.. autoexception:: UCube.LoginFailed
    :members:

==============
Page Not Found
==============
.. autoexception:: UCube.PageNotFound
    :members:

==================
Being Rate Limited
==================
.. autoexception:: UCube.BeingRateLimited
    :members:


.. _account_token:

Get Account Token
=================
There are two ways to log in.
The first way is using a username and password to login which will automatically refresh your token.
The second way is getting your account token manually and will require manual updates about every 6 months.

In order to get your account token, go to https://www.united-cube.com/ and Inspect Element (F12).
Then go to the `Network` tab and filter by `XHR`. Then refresh your page (F5) and look for ``popup`` or ``clubs`` under `XHR`.
Under Headers, scroll to the bottom and view the request headers. You want to copy everything past `Authorization: Bearer`.

For example, you may see (This is just an example):
``Authorization: Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ``
Then ``ABCDEFGHIJKLMNOPQRSTUVWXYZ`` would be your auth token for UCube.
It is suggested to have the auth token as an environment variable.


Asynchronous Usage
==================

.. code-block:: python

    # Asynchronous


Synchronous Usage
=================

.. code-block:: python

    # Synchronous



