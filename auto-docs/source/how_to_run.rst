How to run
==========


Launch Ichnosat
---------------


1. **set installation folder as current directory (e.g. /usr/ichnosat)**


.. code-block:: bash

   cd /usr/ichnosat


2. **launch container**


.. code-block:: bash

   docker-compose up

|


If you are running Ichnosat for the first time, you have to create the database, following these steps:

2.1. **Wait when Postgres server is ready to receive queries:**

Check the logs in the terminal where docker-compose has been launched and wait the log 'database system is ready to accept connections'

|
|

.. image:: _static/db_ready.png
   :align: center
   :width: 550 px

|
|

2.2. **Open the gui client at**  `http://localhost:5040 <http://localhost:5040>`_

When the page is loaded, the dialog of first installation appears:


|
|

.. image:: _static/first_installation_dialog.png
   :align: center
   :width: 400 px

|
|

2.3. **Click on the button 'Create Database':**

|
|

.. image:: _static/first_installation_dialog_create_database.png
   :align: center
   :width: 400 px

|
|

2.4. **Wait database creation:**

|
|

.. image:: _static/creating_database.png
   :align: center
   :width: 400 px

|
|

2.5. **Click on 'Finish' button:**

|
|

.. image:: _static/creating_database_finish.png
   :align: center
   :width: 400 px

|
|

Now Ichnosat is ready to download and process satellite products.

|
|

.. image:: _static/gui_home.png
   :align: center
   :width: 400 px

|
|


Run Downloader
--------------

1. **Click on '+' of *Modules* voice in side bar on the left:**

|
|

.. image:: _static/modules_sidebar.png
   :align: center
   :width: 400 px

|
|

2. **Click on 'Downloader' menu item:**

|
|

.. image:: _static/downloader_section.png
   :align: center
   :width: 400 px

|
|

3. **Start ichnosat clicking on 'Start process' button:**

|
|

.. image:: _static/start_ichnosat.png
   :align: center
   :width: 400 px

|
|


Monitor activities via gui and console
--------------------------------------

To monitor progress activities check the lists of products on Graphica User Interface, logs and file system,
as shown in the following steps:

1. **Check pending products in the GUI**

The pending products are the products that Ichnosat are available to download, but are waiting to download
by the *Downloader*. To see the list of pending products, click on 'Pending' item of 'Products' void in the side bar:

|
|

.. image:: _static/pending_products.png
   :align: center
   :width: 400 px

|
|


2. **Check downloading products in the GUI**

You will find the downloading products list via GUI:

|
|

.. image:: _static/downloading_products.png
   :align: center
   :width: 400 px

|
|


You could also check the progress of download via command line (Unix systems), monitoring
the file size of downloading products. The downloading and downloaded products are located in the folder
'/usr/ichnosat/data_local/inbox'

2.1. **Set inbox folder as current directory**

.. code-block:: bash

   cd /usr/ichnosat/data_local/

2.2. **Monitor download progress via bash scripting (Unix Systems)**


.. code-block:: bash

   while sleep 2; do echo " -------- " &&  du -a ./inbox/; done

|
|

.. image:: _static/monitor_inbox.png
   :align: center
   :width: 400 px

|
|



3. **Check processing products in the GUI**

You will find the processing products on-going list via GUI:

|
|

.. image:: _static/processing_products.png
   :align: center
   :width: 400 px

|
|


You could also check the progress of processing via command line (Unix systems), monitoring
the file size present in the processor folder. The processing and processed products are located in the folder
'/usr/ichnosat/data_local/outbox'

2.1. **Set inbox folder as current directory**

.. code-block:: bash

   cd /usr/ichnosat/data_local/

2.2. **Monitor processing progress via bash scripting (Unix Systems)**


.. code-block:: bash

   while sleep 2; do echo " -------- " &&  du -a ./outbox/; done

|
|

.. image:: _static/monitor_outbox.png
   :align: center
   :width: 400 px

|
|


Monitor activities via logs
---------------------------

Detailed logs are streamed in the 'ichnosat.log' file. The location of this file is
'/usr/ichnosat/data_local/log/ichnosat.log'.

You can watch the stream of logs via command line:

.. code-block:: bash

   cd /usr/ichnosat/data_local/log
   tail -f ichnosat.log


|
|

.. image:: _static/log_example.png
   :align: center
   :width: 400 px

|
|


Open processed product
----------------------

The processed products are located in the '/usr/ichnosat/data_local/outbox' folder.
Every product is a folder with the name composed via the tile name, sensing time, and Processor plugin name.
Like: 'tiles-32-T-ML-2016-7-28-1-NDVI'
where:

- **32-T-ML** is the tile id
- **2016-7-28** is the sensing date
- **-1-** is the processing id (of data provider)
- **NDVI** is the Plugin name, in this example it is a Normalized Difference Vegetation Index product

|
|

.. image:: _static/processed_product.png
   :align: center
   :width: 550 px

|
|

You can open the product with your preferred program:

|
|

.. image:: _static/processed_product_preview.png
   :align: center
   :width: 550 px

|
|