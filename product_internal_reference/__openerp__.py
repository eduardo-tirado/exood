# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Acysos S.L. (http://acysos.com) All Rights Reserved.
#                       Ignacio Ibeas <ignacio@acysos.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "Product Partner Reference",
    "version" : "1.0",
    "author" : "Acysos S.L. sponsored by Gatakka and Polux",
    "website" : "www.acysos.com, gatakka.net",
    "category": 'Generic Modules/Inventory Control',
    "description": """Field to add the partner reference when is different to the internal reference""",
    "license" : "AGPL-3",
    "depends" : ["base", "product"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" :["views/product_view.xml"],
    "active": False,
    "installable": True
}