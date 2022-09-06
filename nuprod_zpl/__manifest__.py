# -*- coding: utf-8 -*-
{
    'name': "nuprod_zpl",

    'summary': """
        Add zpl support""",

    'description': """
        Add zpl support for odoo
    """,

    'author': "Nuprod",
    'website': "https://www.nuprod.fr",

    "category": "Accounting",
    'version': '0.1',
    "license": "AGPL-3",
    'installable': True,

    'depends': ['base','product'],

    'data': [
        'security/ir.model.access.csv',
        'views/report_socket_view.xml',
        'views/stock_product_view.xml',
    ],
}
