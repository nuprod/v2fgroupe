# -*- coding: utf-8 -*-
# Create by Romain Frucco 2/11/22

{
    'name': "nuprod_solidworks_link",

    'summary': """
        Create a link between odoo and solidworks""",

    'description': """
        Let user know about files in solidworks, version and download them
    """,

    'author': "NUprod",
    'website': "https://www.nuprod.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    "license": "AGPL-3",
    'installable': True,

    'depends': ['product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
