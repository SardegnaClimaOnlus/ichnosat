Installation and Requirements
=============================

Software Requirements
---------------------
Before you start you need a working `Docker <https://www.docker.com/>`_  and `Docker Compose <https://docs.docker.com/compose/>`_
installation on the machine where you are going to install Ichnosat.
To install Docker and Docker Compose please follow the relevant instructions for your operating system on the
official documentation:

- `Docker Installation <https://docs.docker.com/engine/installation/>`_
- `Docker  Compose  Installation <https://docs.docker.com/compose/install/>`_

Skills
------
You need to be able to use basic console commands, since the primary purpose of Ichnosat platform is to
process EO satellite images, you will also need to understand the basics of satellite data structure and image processing.

In addition, if you want to extend Ichnosat platform creating a new addon, you should be able to develop
in C++ programming language, using `GDAL <http://www.gdal.org/>`_ library and having a basic knowledge of
`Python <https://www.python.org/>`_ programming.


Download and Installation (Linux/MacOS)
-------------------------

Download
~~~~~~~~
Download the source code package: `zip package  <https://github.com/SardegnaClimaOnlus/ichnosat/archive/master.zip>`_

.. code-block:: bash

   wget https://github.com/SardegnaClimaOnlus/ichnosat/archive/master.zip

Install
~~~~~~~

1. unzip the package
.. code-block:: bash

   unzip ichnosat-master.zip

#. create the working directory (in this example: /usr/ichnosat

.. code-block:: bash

   mkdir -p /usr/ichnosat

#. move ichnosat source code from unzipped folder to working directory, and set as current directory

.. code-block:: bash

   mv ichnosat-master/* /usr/ichnosat
   cd /usr/ichnosat

#. build docker images

.. code-block:: bash

   docker-compose build

This step might take time (10-30 min), building dependencies and local code.






