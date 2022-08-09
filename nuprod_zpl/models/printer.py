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

    def print_report(self, id, data):
        """Print epl report
        :param data: unicode string to print
        """
        printer = self.browse(id)
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
        for record in self:
            if record.barcode:
                dpmm = 8
                label = zplNuprod.Label(51, 30, dpmm)
                height = 0
                char_size = 6
                barcode_width = 3.5
                label.origin(25, 4, '0')
                label.write_text(record.default_code, char_height=char_size, char_width=char_size, justification='C')
                label.endorigin()
                height += 10
                # l.origin((len(record.barcode)*barcode_width)/2,height)
                label.origin(27, height)
                label.write_barcode(height=60, barcode_type='Q', magnification=6)
                label.write_text(record.barcode, qrcode=True)
                label.endorigin()
                connection_printer = self.env["epl.printer"].connection(1)
                self.env["epl.printer"].print_report(1, (bytes(label.dumpZPL(), "utf8")))
            else:
                raise UserError(
                            _(
                                "Pas de code barre sur le produit " + str(record.default_code) + "\n" +
                                "Veuillez en définir un pour imprimer l'étiquette"
                            )
                        )