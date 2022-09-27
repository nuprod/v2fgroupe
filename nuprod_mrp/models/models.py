# -*- coding: utf-8 -*-


from odoo import fields, models, _

import logging

_logger = logging.getLogger(__name__)

class ProductProductNuprod(models.Model):
    _inherit = 'product.product'
    _description = 'Product MRP Surchage'

    def button_bom_cost(self):
        self.ensure_one()
        self._set_price_from_bom()
        return True