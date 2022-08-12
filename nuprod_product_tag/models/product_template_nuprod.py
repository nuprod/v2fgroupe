# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class productTemplateNuprod(models.Model):

    _inherit = "product.template"

    product_tag_ids = fields.Many2many('product.tag.nuprod', 'product_tag_product_template_rel', string='Product Tags')