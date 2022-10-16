# -*- coding: utf-8 -*-
{
    'name': "nuprod_mrp",

    'summary': """
        Add functionnality to mrp module""",

    'description': """
        Add return True on button_bom_cost
    """,

    'author': "NUprod",
    'website': "https://www.nuprod.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp', 'product'],

    # always loaded
    'data': [
        #    'security/ir.model.access.csv',
            'views/views.xml',
        #  'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
