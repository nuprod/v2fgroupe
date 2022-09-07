# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import socket
from . import zplNuprod
from odoo.exceptions import UserError

class nuprod_zpl(models.Model):

    _description = 'nuprod_zpl'
    _name = "epl.printer"

    name = fields.Char('name', size=256, required=True)
    ip_address = fields.Char('Ip Address', size=32, required=True)
    port = fields.Integer('Port', required=True)
    companyLocalisation = fields.Many2one(
        comodel_name="res.company",
        inverse_name="name",
        string="Localisation in company")
    logger = logging.getLogger(__name__)
    logger.warning('Nuprod ZPL Load')

    def connection(self, printer_id):
        printer = self.browse(printer_id)

        ip = printer.ip_address
        port = printer.port
        # buffer_size = printer.buffer_size

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = {
            'socket': s,
            'ip': ip,
            'port': port,
        }
        return res

    def print_report(self, idCompany, data):
        logger = logging.getLogger(__name__)
        """Print epl report
        :param data: unicode string to print
        """
        printer = self.search([('companyLocalisation', "=", idCompany)])
        logger.warning("Id imprimante:" + str(printer.id))

        if not printer:
            raise Warning(_("Printer not found"))
        port = printer.port
        ip = printer.ip_address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data)
            s.close()
        except Exception as e:
            print("Couldn't send epl printing: %s" % e)
            # logger.error('Failed to do something: ' + str(e))

class nuprod_print_product(models.Model):

    _inherit = "product.template"

    def print_label_nuprod(self):
        logger = logging.getLogger(__name__)
        product_without_barcode = []
        for record in self:
            if record.barcode:
                dpmm = 8
                label = zplNuprod.Label(56, 30, dpmm)
                height = 0
                char_size = 6
                margeGauche = 10
                largeurEtiquette = 102
                if (margeGauche + (largeurEtiquette - (len(record.default_code) * char_size)) / 2) < 0:
                    x_Origin = margeGauche
                else:
                    x_Origin = (largeurEtiquette - (len(record.default_code) * char_size)) / 2
                label.origin(x_Origin, 4, '0')
                label.write_text(record.default_code, char_height=char_size, char_width=char_size, justification='C')
                label.endorigin()
                height += 10
                label.origin(27, height)
                label.write_barcode(height=60, barcode_type='Q', magnification=6)
                label.write_text(record.barcode, qrcode=True)
                label.endorigin()
                connection_printer = self.env["epl.printer"].connection(1)
                logger.warning(connection_printer)
                self.env["epl.printer"].print_report(1, (bytes(label.dumpZPL(), "utf8")))
            else:
                product_without_barcode.append(str(record.name))

        if len(product_without_barcode) > 0:
            title = _("Barcode problem on product")
            message = _("No barcode on product " + str(product_without_barcode))
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'sticky': True,
                }
            }