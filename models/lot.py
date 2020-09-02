from collections import defaultdict
from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from re import findall as regex_findall, split as regex_split

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class InheritStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def create(self, vals):
        print(vals)
        print(vals.get('lot_id'))
        print(vals.get('product_id'))
        # pro_id = vals.get('product_id')

        pro_obj = self.env['product.product'].search([('id', '=', vals.get('product_id'))])
        tracking_type = pro_obj[0].product_tmpl_id.tracking
        com_id = pro_obj[0].product_tmpl_id.company_id
        print("Tracking type: ,", tracking_type)
        print("Company Id: ", com_id)
        print(pro_obj[0])

        if tracking_type != 'none' and vals.get('qty_done'):
            # if tracking_type == 'lot':
            print("Create Lot for products")
            lot_vals = {
                'company_id': self.env.company.id,
                'name': self.env['ir.sequence'].next_by_code('serial.lot.sequence') or _('New'),
                'product_id': vals['product_id'],
                'product_qty': vals['qty_done'],
            }
            obj_lot = self.env['stock.production.lot'].create(lot_vals)
            print("object of stock.production.lot: ", obj_lot)
            vals['lot_id'] = obj_lot.id

        print(vals)

        mls = super(InheritStockMoveLine, self).create(vals)

        return mls




class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_stock_moves(self, picking):
        self.ensure_one()
        res = super(InheritPurchaseOrderLine, self)._prepare_stock_moves(picking)

        for rec in res:

            pro_name = rec['name']
            pro_id = rec['product_id']
            pro_qty = rec['product_uom_qty']
            dt = rec['date']
            com_id = rec['company_id'] or self.env.company.id

            # data = self.env['product.packaging'].search([('product_id', '=', pro_id), ]) user product instead of data
            data = self.env['product.product'].search([('id', '=', pro_id)])

            print("product_id: ", pro_id)
            print(data)
            obj_lot = self.env['stock.production.lot'].search([('product_id', '=', pro_id)])
            tracking_type = data[0].product_tmpl_id.tracking
            if tracking_type != 'none':  # yha serail no and lot no ke hisab se generate krne pdhege
                stock_move_line_vals = {
                    'company_id': self.env.company.id,
                    'location_dest_id': rec['location_dest_id'],
                    'location_id': rec['location_id'],
                    'product_uom_id': rec['product_uom'],
                    'product_id': pro_id,
                    'picking_id': rec['picking_id'],
                    'lot_name': tracking_type,
                    'qty_done': rec['product_uom_qty'],
                }
                rec['move_line_nosuggest_ids'] = [(0, 0, stock_move_line_vals),]

        print(res)
        return res

