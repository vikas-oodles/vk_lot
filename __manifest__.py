{
    'name': 'SerialLot Creation',
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Module for serial or lot creation',
    'sequence': '55',
    'author': 'vikas kumar',
    'maintainer': 'odoo mates',
    'website': 'odoomate.com',
    'depends': ["base", "sale_management", "stock", "account", "mail", "sale", "purchase", 'mrp'],
    'demo': [],
    'data': [
        'views/product.xml',
        'views/lot.xml',
        'data/sequence.xml',

    ],
    'installable': True,
    'application': True,
    'auto-install': False,

}