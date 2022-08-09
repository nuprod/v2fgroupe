# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class epl_report(models.Model):
    _name = 'epl.report'
    id = fields.Integer('ID')
    name = fields.Char('Name', size=128, required=True)
    printer_id = fields.Many2one(
            'epl.printer',
            'Printer', required=True)
    template = fields.Text('Template', required=True)