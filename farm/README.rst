.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Farm
==============


This module was written to to control the process and cost of an animal farm for the production of meat products.
It allows full traceability of lots of animals and foods that are fed well as origin (parents).
Animals remains localized and the phase in which they are.
Imputed costs of food, medication and general expenses to determine the net profit of the sales.

Installation
============

To install this module, you need to:

* clone the branch 8.0 of the repository https://github.com/OCA/vertical-agriculture
* add the path to this repository in your configuration (addons-path)
* update the module list
* search for "farm" in your addons
* install the module


Usage
=====

To use this module, you need to:

* product
* stock
* mrp
* mrp_lot_cost (Revisar si mandar al repositorio de mrp o dejar aqui)

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/{repo_id}/{branch}

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* semen_extraction does not pick materials of correct stock.location


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
https://github.com/OCA/vertical-agriculture/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
https://github.com/OCA/vertical-agriculture/issues/new?body=module:%20
farm%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Alexander Ezquevo <alexander@acysos.com>

Based in module farm of tryton developed by NaN·tic 

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.