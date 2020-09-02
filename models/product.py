from odoo import models, api, fields, _


class ProductDetail(models.Model):
    _name = 'product.detail'
    _description = 'Product Detail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    product_name = fields.Char(string='Product Name', required=True)
    product_type = fields.Selection([
        ('electronic', 'Electronic'),
        ('wooden', 'Wooden'),
        ('metal', 'Metal'),
    ], string='Product Type', default='metal')
    product_price = fields.Integer("Product Price")



