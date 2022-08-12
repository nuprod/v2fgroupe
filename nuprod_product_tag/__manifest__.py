# -*- coding: utf-8 -*-
{
    'name': "nuprod_product_tag",

    'summary': """
        Add product tag functionality""",

    'description': """
        Add product tag functionality
    """,

    'author': "Nuprod",
    'website': "https://www.nuprod.fr",

    "category": "stock",
    'version': '0.1',
    "license": "AGPL-3",
    'installable': True,

    'depends': ['product'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template_nuprod.xml',
        'views/product_tag_view_nuprod.xml',
        #'views/templates.xml',
    ],
}
