How to configure
================

Introduction
------------

How to configure the downloader
-------------------------------




Set Tiles to download
~~~~~~~~~~~~~~~~~~~~~
1. Edit the *Downloader* configuration file

.. code-block:: bash

   vim /usr/ichnosat/src/core/downloader/config/config.cfg

2. Set the list of tiles using the comma ',' as separator, in the 'tiles' key; e.g.:


.. code-block:: bash

   tiles=32/T/ML,32/T/NL,32/T/MK,32/T/NK,32/S/MJ,32/S/NJ



Set files to download for each tile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Edit the *Downloader* configuration file

.. code-block:: bash

   vim /usr/ichnosat/src/core/downloader/config/config.cfg

2. Set the list of tiles using the comma ',' as separator, in the 'files_to_download' key; e.g.:


.. code-block:: bash

   files_to_download=B04.jp2,B08.jp2

Set Sensing time interval
~~~~~~~~~~~~~~~~~~~~~~~~~
You can filter the products to download, setting the sensing time interval.
The interval is composed of *start* date and *end* date.

1. Edit the *Downloader* configuration file

.. code-block:: bash

   vim /usr/ichnosat/src/core/downloader/config/config.cfg

2. Set the sensing time **start**, in the 'start_date' key; e.g.:


.. code-block:: bash

   start_date=2016/07/13


3. Set the sensing time **end**, in the 'end_date' key; e.g.:


.. code-block:: bash

   end_date=2017/07/13

It is possible to set *NOW* as sensing time *end*, this means that the *Downloader* for every download cycle consider as sensing time *end* the current date; e.g.:

.. code-block:: bash

   end_date=NOW

Set how many parallels download threads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can define how many parallels download run in the same time:

1. Edit the *Downloader* configuration file

.. code-block:: bash

   vim /usr/ichnosat/src/core/downloader/config/config.cfg

2. Set how many threads the *Downloader* launches, in the 'parallel_downloads' key; e.g.:


.. code-block:: bash

   parallel_downloads=2

How to configure the processor
------------------------------

Set how many parallels processing threads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can define how many parallels processing run in the same time:

1. Edit the *Processor* configuration file

.. code-block:: bash

   vim /usr/ichnosat/src/core/processing_pipe/config/config.cfg

2. Set how many threads the *Processor* launches, in the 'parallel_processing' key; e.g.:


.. code-block:: bash

   parallel_processing=2

How to configure the global platform parameters
-----------------------------------------------

How to configure the cron
-------------------------
Ichnosat exploit linux cron to run periodically the process.

1. Edit the *System Manager* configuration file

.. code-block:: bash

   vim /usr/ichnosat/src/core/system_manager/config/config.cfg

2. Set the cron string, in the 'cron' key; e.g.:


.. code-block:: bash

   cron = 10 10 * * *

How to configure the graphical user interface port
--------------------------------------------------
Using Docker and Docker Compose, you can set the port of GUI client:

1. Edit the docker-compose.yml configuration file

.. code-block:: bash

   vim /usr/ichnosat/docker-compose.yml

2. Set the port number, in the 'ports' property; e.g. (in this example is 5040):


.. code-block:: bash

     nginx:
        image: nginx
        volumes:
        - ./src/gui:/usr/share/nginx/html
        ports:
        - "5040:80"

