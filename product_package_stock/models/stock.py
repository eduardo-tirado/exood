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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import SUPERUSER_ID, api
import math

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    @api.cr_uid_ids_context
    def do_transfer(self, cr, uid, picking_ids, context=None):
        super(stock_picking, self).do_transfer(cr, uid, picking_ids, context)
        for picking in self.browse(cr, uid, picking_ids, context):
            for move in picking.move_lines:
                if move.product_id.package_id:
                    if move.product_id.package_id.uos_id:
                        uos_id = move.product_id.package_id.uos_id.id
                    else:
                        uos_id = move.product_id.package_id.uom_id.id
                         
                    defaults_package = {
                        'product_id': move.product_id.package_id.id,
                        'product_qty' : math.ceil(product_qty/move.product_id.pack_quantity),
                        'product_uos_qty': math.ceil(product_qty/move.product_id.pack_quantity),
                        'picking_id' : new_picking,
                        'state': 'assigned',
                        'move_dest_id': False,
                        'origin': move.origin,
                        'address_id':move.address_id.id,
                        'product_uom':move.product_id.uom_id.id,
                        'date_expected':move.date_expected,
                        'product_uos':uos_id,
                        'location_id':move.location_id.id,
                        'name':move.product_id.package_id.name,
                        'note':move.note,
                        'partner_id':move.partner_id.id,
                        'company_id':move.company_id.id,
                        'priority':move.priority,
                        'location_dest_id':move.location_dest_id.id,
                        'sale_line_id':move.sale_line_id.id,
                        'weight':move.product_id.package_id.weight*math.ceil(product_qty/move.product_id.pack_quantity),
                        'weight_net':move.product_id.package_id.weight_net*math.ceil(product_qty/move.product_id.pack_quantity),
                    }
                    move_obj.create(cr, uid, defaults_package)
        return True
                
    
#     def do_partial(self, cr, uid, ids, partial_datas, context=None):
#         """ Makes partial picking and moves done.
#         @param partial_datas : Dictionary containing details of partial picking
#                           like partner_id, address_id, delivery_date,
#                           delivery moves with product_id, product_qty, uom
#         @return: Dictionary of values
#         """
#         
#         if context is None:
#             context = {}
#         else:
#             context = dict(context)
#         res = {}
#         move_obj = self.pool.get('stock.move')
#         product_obj = self.pool.get('product.product')
#         currency_obj = self.pool.get('res.currency')
#         uom_obj = self.pool.get('product.uom')
#         sequence_obj = self.pool.get('ir.sequence')
#         wf_service = netsvc.LocalService("workflow")
#         for pick in self.browse(cr, uid, ids, context=context):
#             new_picking = None
#             complete, too_many, too_few = [], [], []
#             move_product_qty = {}
#             prodlot_ids = {}
#             product_avail = {}
#             for move in pick.move_lines:
#                 if move.state in ('done', 'cancel'):
#                     continue
#                 partial_data = partial_datas.get('move%s'%(move.id), {})
#                 #Commented in order to process the less number of stock moves from partial picking wizard
#                 #assert partial_data, _('Missing partial picking data for move #%s') % (move.id)
#                 product_qty = partial_data.get('product_qty') or 0.0
#                 move_product_qty[move.id] = product_qty
#                 product_uom = partial_data.get('product_uom') or False
#                 product_price = partial_data.get('product_price') or 0.0
#                 product_currency = partial_data.get('product_currency') or False
#                 prodlot_id = partial_data.get('prodlot_id') or False
#                 prodlot_ids[move.id] = prodlot_id
#                 if move.product_qty == product_qty:
#                     complete.append(move)
#                 elif move.product_qty > product_qty:
#                     too_few.append(move)
#                 else:
#                     too_many.append(move)
# 
#                 # Average price computation
#                 if (pick.type == 'in') and (move.product_id.cost_method == 'average'):
#                     product = product_obj.browse(cr, uid, move.product_id.id)
#                     move_currency_id = move.company_id.currency_id.id
#                     context['currency_id'] = move_currency_id
#                     qty = uom_obj._compute_qty(cr, uid, product_uom, product_qty, product.uom_id.id)
# 
#                     if product.id in product_avail:
#                         product_avail[product.id] += qty
#                     else:
#                         product_avail[product.id] = product.qty_available
# 
#                     if qty > 0:
#                         new_price = currency_obj.compute(cr, uid, product_currency,
#                                 move_currency_id, product_price)
#                         new_price = uom_obj._compute_price(cr, uid, product_uom, new_price,
#                                 product.uom_id.id)
#                         if product.qty_available <= 0:
#                             new_std_price = new_price
#                         else:
#                             # Get the standard price
#                             amount_unit = product.price_get('standard_price', context)[product.id]
#                             new_std_price = ((amount_unit * product_avail[product.id])\
#                                 + (new_price * qty))/(product_avail[product.id] + qty)
#                         # Write the field according to price type field
#                         product_obj.write(cr, uid, [product.id], {'standard_price': new_std_price})
# 
#                         # Record the values that were chosen in the wizard, so they can be
#                         # used for inventory valuation if real-time valuation is enabled.
#                         move_obj.write(cr, uid, [move.id],
#                                 {'price_unit': product_price,
#                                  'price_currency_id': product_currency})
# 
# 
#             for move in too_few:
#                 product_qty = move_product_qty[move.id]
# 
#                 if not new_picking:
#                     sequence = pick.type
#                     if sequence == 'out':
#                         sequence = 'sent'
#                     new_picking = self.copy(cr, uid, pick.id,
#                             {
#                                 'name': sequence_obj.get(cr, uid, 'stock.picking.%s'%(sequence)),
#                                 'move_lines' : [],
#                                 'state':'draft',
#                                 'type':'out'
#                             })
#                 if product_qty != 0:
#                     defaults = {
#                             'product_qty' : product_qty,
#                             'product_uos_qty': product_qty, #TODO: put correct uos_qty
#                             'picking_id' : new_picking,
#                             'state': 'assigned',
#                             'move_dest_id': False,
#                             'price_unit': move.price_unit,
#                     }
#                     prodlot_id = prodlot_ids[move.id]
#                     if prodlot_id:
#                         defaults.update(prodlot_id=prodlot_id)
#                     move_obj.copy(cr, uid, move.id, defaults)
# 
#                 move_obj.write(cr, uid, [move.id],
#                         {
#                             'product_qty' : move.product_qty - product_qty,
#                             'product_uos_qty':move.product_qty - product_qty, #TODO: put correct uos_qty
#                         })
# 
#                 if move.product_id.package_id:
#                     if move.product_id.package_id.uos_id:
#                         uos_id = move.product_id.package_id.uos_id.id
#                     else:
#                         uos_id = move.product_id.package_id.uom_id.id
#                         
#                     defaults_package = {
#                         'product_id': move.product_id.package_id.id,
#                         'product_qty' : math.ceil(product_qty/move.product_id.pack_quantity),
#                         'product_uos_qty': math.ceil(product_qty/move.product_id.pack_quantity),
#                         'picking_id' : new_picking,
#                         'state': 'assigned',
#                         'move_dest_id': False,
#                         'origin': move.origin,
#                         'address_id':move.address_id.id,
#                         'product_uom':move.product_id.uom_id.id,
#                         'date_expected':move.date_expected,
#                         'product_uos':uos_id,
#                         'location_id':move.location_id.id,
#                         'name':move.product_id.package_id.name,
#                         'note':move.note,
#                         'partner_id':move.partner_id.id,
#                         'company_id':move.company_id.id,
#                         'priority':move.priority,
#                         'location_dest_id':move.location_dest_id.id,
#                         'sale_line_id':move.sale_line_id.id,
#                         'weight':move.product_id.package_id.weight*math.ceil(product_qty/move.product_id.pack_quantity),
#                         'weight_net':move.product_id.package_id.weight_net*math.ceil(product_qty/move.product_id.pack_quantity),
#                     }
#                     move_obj.create(cr, uid, defaults_package)
# 
#             if new_picking:
#                 move_obj.write(cr, uid, [c.id for c in complete], {'picking_id': new_picking})
#             for move in complete:
#                 
#                 product_qty = move_product_qty[move.id]
# 
#                 if not new_picking:
#                     sequence = pick.type
#                     if sequence == 'out':
#                         sequence = 'sent'
#                     new_picking = self.copy(cr, uid, pick.id,
#                             {
#                                 'name': sequence_obj.get(cr, uid, 'stock.picking.%s'%(sequence)),
#                                 'move_lines' : [],
#                                 'state':'draft',
#                                 'type':'out'
#                             })
#                 if product_qty != 0:
#                     defaults = {
#                             'product_qty' : product_qty,
#                             'product_uos_qty': product_qty, #TODO: put correct uos_qty
#                             'picking_id' : new_picking,
#                             'state': 'assigned',
#                             'move_dest_id': False,
#                             'price_unit': move.price_unit,
#                     }
#                     prodlot_id = prodlot_ids[move.id]
#                     if prodlot_id:
#                         defaults.update(prodlot_id=prodlot_id)
#                     move_obj.copy(cr, uid, move.id, defaults)
# 
#                 move_obj.write(cr, uid, [move.id],
#                         {
#                             'product_qty' : move.product_qty - product_qty,
#                             'product_uos_qty':move.product_qty - product_qty, #TODO: put correct uos_qty
#                             'state':'done'
#                         })
#                         
#                 if move.product_id.package_id:
#                     if move.product_id.package_id.uos_id:
#                         uos_id = move.product_id.package_id.uos_id.id
#                     else:
#                         uos_id = move.product_id.package_id.uom_id.id
#                         
#                     defaults_package = {
#                         'product_id': move.product_id.package_id.id,
#                         'product_qty' : math.ceil(product_qty/move.product_id.pack_quantity),
#                         'product_uos_qty': math.ceil(product_qty/move.product_id.pack_quantity),
#                         'picking_id' : new_picking,
#                         'state': 'assigned',
#                         'move_dest_id': False,
#                         'origin': move.origin,
#                         'address_id':move.address_id.id,
#                         'product_uom':move.product_id.uom_id.id,
#                         'date_expected':move.date_expected,
#                         'product_uos':uos_id,
#                         'location_id':move.location_id.id,
#                         'name':move.product_id.package_id.name,
#                         'note':move.note,
#                         'partner_id':move.partner_id.id,
#                         'company_id':move.company_id.id,
#                         'priority':move.priority,
#                         'location_dest_id':move.location_dest_id.id,
#                         'sale_line_id':move.sale_line_id.id,
#                         'weight':move.product_id.package_id.weight*math.ceil(product_qty/move.product_id.pack_quantity),
#                         'weight_net':move.product_id.package_id.weight_net*math.ceil(product_qty/move.product_id.pack_quantity),
#                     }
#                     move_obj.create(cr, uid, defaults_package)
#                 
#                 if prodlot_ids.get(move.id):
#                     move_obj.write(cr, uid, [move.id], {'prodlot_id': prodlot_ids[move.id]})
#             for move in too_many:
#                 product_qty = move_product_qty[move.id]
#                 defaults = {
#                     'product_qty' : product_qty,
#                     'product_uos_qty': product_qty, #TODO: put correct uos_qty
#                 }
#                 prodlot_id = prodlot_ids.get(move.id)
#                 if prodlot_ids.get(move.id):
#                     defaults.update(prodlot_id=prodlot_id)
#                 if new_picking:
#                     defaults.update(picking_id=new_picking)
#                 move_obj.write(cr, uid, [move.id], defaults)
# 
# 
#             # At first we confirm the new picking (if necessary)
#             if new_picking:
#                 wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)
#                 # Then we finish the good picking
#                 self.write(cr, uid, [pick.id], {'backorder_id': new_picking})
#                 self.action_move(cr, uid, [new_picking])
#                 wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_done', cr)
#                 wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
#                 delivered_pack_id = new_picking
#             else:
#                 self.action_move(cr, uid, [pick.id])
#                 wf_service.trg_validate(uid, 'stock.picking', pick.id, 'button_done', cr)
#                 delivered_pack_id = pick.id
# 
#             delivered_pack = self.browse(cr, uid, delivered_pack_id, context=context)
#             res[pick.id] = {'delivered_picking': delivered_pack.id or False}
# 
#         return res
#             
#     def action_invoice_create(self, cr, uid, ids, journal_id=False,
#             group=False, type='out_invoice', context=None):
#         """ Creates invoice based on the invoice state selected for picking.
#         @param journal_id: Id of journal
#         @param group: Whether to create a group invoice or not
#         @param type: Type invoice to be created
#         @return: Ids of created invoices for the pickings
#         """
#         if context is None:
#             context = {}
# 
#         invoice_obj = self.pool.get('account.invoice')
#         invoice_line_obj = self.pool.get('account.invoice.line')
#         address_obj = self.pool.get('res.partner.address')
#         invoices_group = {}
#         res = {}
#         inv_type = type
#         for picking in self.browse(cr, uid, ids, context=context):
#             if picking.invoice_state != '2binvoiced':
#                 continue
#             payment_term_id = False
#             partner =  picking.address_id and picking.address_id.partner_id
#             if not partner:
#                 raise osv.except_osv(_('Error, no partner !'),
#                     _('Please put a partner on the picking list if you want to generate invoice.'))
# 
#             if not inv_type:
#                 inv_type = self._get_invoice_type(picking)
# 
#             if inv_type in ('out_invoice', 'out_refund'):
#                 account_id = partner.property_account_receivable.id
#                 payment_term_id = self._get_payment_term(cr, uid, picking)
#             else:
#                 account_id = partner.property_account_payable.id
# 
#             address_contact_id, address_invoice_id = \
#                     self._get_address_invoice(cr, uid, picking).values()
#             address = address_obj.browse(cr, uid, address_contact_id, context=context)
# 
#             comment = self._get_comment_invoice(cr, uid, picking)
#             if group and partner.id in invoices_group:
#                 invoice_id = invoices_group[partner.id]
#                 invoice = invoice_obj.browse(cr, uid, invoice_id)
#                 invoice_vals = {
#                     'name': (invoice.name or '') + ', ' + (picking.name or ''),
#                     'origin': (invoice.origin or '') + ', ' + (picking.name or '') + (picking.origin and (':' + picking.origin) or ''),
#                     'comment': (comment and (invoice.comment and invoice.comment+"\n"+comment or comment)) or (invoice.comment and invoice.comment or ''),
#                     'date_invoice':context.get('date_inv',False),
#                     'user_id':uid
#                 }
#                 invoice_obj.write(cr, uid, [invoice_id], invoice_vals, context=context)
#             else:
#                 invoice_vals = {
#                     'name': picking.name,
#                     'origin': (picking.name or '') + (picking.origin and (':' + picking.origin) or ''),
#                     'type': inv_type,
#                     'account_id': account_id,
#                     'partner_id': address.partner_id.id,
#                     'address_invoice_id': address_invoice_id,
#                     'address_contact_id': address_contact_id,
#                     'comment': comment,
#                     'payment_term': payment_term_id,
#                     'fiscal_position': partner.property_account_position.id,
#                     'date_invoice': context.get('date_inv',False),
#                     'company_id': picking.company_id.id,
#                     'user_id':uid
#                 }
#                 cur_id = self.get_currency_id(cr, uid, picking)
#                 if cur_id:
#                     invoice_vals['currency_id'] = cur_id
#                 if journal_id:
#                     invoice_vals['journal_id'] = journal_id
#                 invoice_id = invoice_obj.create(cr, uid, invoice_vals,
#                         context=context)
#                 invoices_group[partner.id] = invoice_id
#             res[picking.id] = invoice_id
#             pack_category = self.pool.get('product.category').search(cr,uid,[('name','=','Package')])
#             for move_line in picking.move_lines:
#                 if not move_line.product_id.categ_id.id in pack_category:
#                     if move_line.state == 'cancel':
#                         continue
#                     origin = move_line.picking_id.name or ''
#                     if move_line.picking_id.origin:
#                         origin += ':' + move_line.picking_id.origin
#                     if group:
#                         name = (picking.name or '') + '-' + move_line.name
#                     else:
#                         name = move_line.name
#     
#                     if inv_type in ('out_invoice', 'out_refund'):
#                         account_id = move_line.product_id.product_tmpl_id.\
#                                 property_account_income.id
#                         if not account_id:
#                             account_id = move_line.product_id.categ_id.\
#                                     property_account_income_categ.id
#                     else:
#                         account_id = move_line.product_id.product_tmpl_id.\
#                                 property_account_expense.id
#                         if not account_id:
#                             account_id = move_line.product_id.categ_id.\
#                                     property_account_expense_categ.id
#     
#                     price_unit = self._get_price_unit_invoice(cr, uid,
#                             move_line, inv_type)
#                     discount = self._get_discount_invoice(cr, uid, move_line)
#                     tax_ids = self._get_taxes_invoice(cr, uid, move_line, inv_type)
#                     account_analytic_id = self._get_account_analytic_invoice(cr, uid, picking, move_line)
#     
#                     #set UoS if it's a sale and the picking doesn't have one
#                     uos_id = move_line.product_uos and move_line.product_uos.id or False
#                     if not uos_id and inv_type in ('out_invoice', 'out_refund'):
#                         uos_id = move_line.product_uom.id
#                     account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, partner.property_account_position, account_id)
#                     invoice_line_id = invoice_line_obj.create(cr, uid, {
#                         'name': name,
#                         'origin': origin,
#                         'invoice_id': invoice_id,
#                         'uos_id': uos_id,
#                         'product_id': move_line.product_id.id,
#                         'account_id': account_id,
#                         'price_unit': price_unit,
#                         'discount': discount,
#                         'quantity': move_line.product_uos_qty or move_line.product_qty,
#                         'invoice_line_tax_id': [(6, 0, tax_ids)],
#                         'account_analytic_id': account_analytic_id,
#                     }, context=context)
#                     self._invoice_line_hook(cr, uid, move_line, invoice_line_id)
# 
#             invoice_obj.button_compute(cr, uid, [invoice_id], context=context,
#                     set_total=(inv_type in ('in_invoice', 'in_refund')))
#             self.write(cr, uid, [picking.id], {
#                 'invoice_state': 'invoiced',
#                 }, context=context)
#             self._invoice_hook(cr, uid, picking, invoice_id)
#         self.write(cr, uid, res.keys(), {
#             'invoice_state': 'invoiced',
#             }, context=context)
#         return res
    
