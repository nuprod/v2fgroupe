# coding: utf-8
# Copyright 2022 NUprod (<https://www.nuprod.fr>)

import socket
import json
import logging
from datetime import datetime
import base64

from odoo import _, api, models, fields
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class nuprodSolidworksLink(models.Model):

    _inherit = "product.template"

    infos_3d_lines = fields.One2many(
        "nuprod.solidworks.link", "product_id", string="Results", store=True
    )

    def file_info_pdm(self):
        logger.error("Nuprod Solidworks start")
        # connection au server de fichier sur le pdm serveur
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("185.138.148.117", 8000))
        # init des variables
        datas_from_pdm = []
        toDelete = []
        file_name = self.default_code
        # envoi de la requette
        message = str.encode(json.dumps({"filename": file_name, "mode": "readInfo"}))
        s.send(message)
        # reception de la réponse
        datas_from_pdm = s.recv(4096).decode()
        # si ça répond
        if datas_from_pdm:
            # tant qu'on à pas la fin du message
            while datas_from_pdm[-1] != '#':
                datas_from_pdm += s.recv(4096).decode()
            drawing_vals = []
            # on éclate la réponse 
            new_datas = datas_from_pdm[2:-3].split("), (")
            for new_data in new_datas:
                # on éclate en ligne
                new_data = (new_data.split(", "))
                # si la ligne n'est pas crée
                is_drawing = self.env["nuprod.solidworks.link"].search([("id_3D_base", "=", new_data[0])])
                # datas_odoo.append({'drawing': new_data[1][-1:-1], 'date': new_data[4][-4:] + "-" + new_data[5] + "-" + new_data[6]})
                if is_drawing.id is False:
                    # on la crée
                    drawing_vals.append((0, 0, {"id_3D_base": new_data[0], "drawing": new_data[1][1:-1],
                                        "creation_date": datetime.strptime((new_data[4][-4:] + "-" + new_data[5] + "-" + new_data[6][:1]), "%Y-%m-%d")}))
            lenDrawing = len(drawing_vals)
            # je traite les doublons
            for i in range(0, lenDrawing):
                for j in range(i + 1, lenDrawing):
                    if (drawing_vals[i][2]['drawing'] == drawing_vals[j][2]['drawing']):
                        toDelete.append(j)
            new_drawing_vals = [j for i, j in enumerate(drawing_vals) if i not in toDelete]
            # on envoi les lignes
            self.infos_3d_lines = new_drawing_vals
            logger.info(new_drawing_vals)
        else:
            raise UserError(_("Nothing in the PDM"))
        s.close()

class nuprodSolidworksLinkProduct(models.Model):

    _inherit = "product.product"

    infos_3d_lines = fields.One2many(
        "nuprod.solidworks.link", "product_id", string="Results", store=True
    )

    def file_info_pdm(self):
        logger.error("Nuprod Solidworks start")
        # connection au server de fichier sur le pdm serveur
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("185.138.148.117", 8000))
        # init des variables
        datas_from_pdm = []
        toDelete = []
        file_name = self.default_code
        # envoi de la requette
        message = str.encode(json.dumps({"filename": file_name, "mode": "readInfo"}))
        s.send(message)
        # reception de la réponse
        datas_from_pdm = s.recv(4096).decode()
        # si ça répond
        if datas_from_pdm:
            # tant qu'on à pas la fin du message
            while datas_from_pdm[-1] != '#':
                datas_from_pdm += s.recv(4096).decode()
            drawing_vals = []
            # on éclate la réponse 
            new_datas = datas_from_pdm[2:-3].split("), (")
            for new_data in new_datas:
                # on éclate en ligne
                new_data = (new_data.split(", "))
                # si la ligne n'est pas crée
                is_drawing = self.env["nuprod.solidworks.link"].search([("id_3D_base", "=", new_data[0])])
                # datas_odoo.append({'drawing': new_data[1][-1:-1], 'date': new_data[4][-4:] + "-" + new_data[5] + "-" + new_data[6]})
                if is_drawing.id is False:
                    # on la crée
                    drawing_vals.append((0, 0, {"id_3D_base": new_data[0], "drawing": new_data[1][1:-1],
                                        "creation_date": datetime.strptime((new_data[4][-4:] + "-" + new_data[5] + "-" + new_data[6][:1]), "%Y-%m-%d")}))
            lenDrawing = len(drawing_vals)
            # je traite les doublons
            for i in range(0, lenDrawing):
                for j in range(i + 1, lenDrawing):
                    if (drawing_vals[i][2]['drawing'] == drawing_vals[j][2]['drawing']):
                        toDelete.append(j)
            new_drawing_vals = [j for i, j in enumerate(drawing_vals) if i not in toDelete]
            # on envoi les lignes
            self.infos_3d_lines = new_drawing_vals
            logger.info(new_drawing_vals)
        else:
            raise UserError(_("Nothing in the PDM"))
        s.close()

class solidworksBase(models.Model):

    _name = "nuprod.solidworks.link"
    _description = "Base Drawing 3D"

    product_id = fields.Many2one(
        "product.template", "Product")

    id_3D_base = fields.Integer()
    drawing = fields.Char("drawing")
    creation_date = fields.Date("Creation date")

    def download_file(self):
        logger.error("Download File")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("185.138.148.117", 8000))
            message = str.encode(json.dumps({"id_base": self.id_3D_base, "mode": "downloadFile"}))
            s.send(message)

            data = bytearray()
            fragment = []

            # Recupération du fichier avec son nom
            firstPart = s.recv(20).decode().split('#')
            drawingFilename = firstPart[0]
            # Transfert du morceau d'info restant
            try:
                fragment.append(firstPart[1].encode())
                while True:
                    r = s.recv(4096)
                    if r == b'':
                        break
                    fragment.append(r)

                file = (b"".join(fragment))

                attachment = self.env['ir.attachment'].create({
                    'type': 'binary',
                    'name': drawingFilename,
                    'res_model': 'ir.actions.report',
                    'res_name': 'Drawing',
                    'res_id': self[0].id,
                    'datas': base64.encodebytes(file),
                })

                return {
                    'name': 'Drawing' + str(drawingFilename),
                    'type': 'ir.actions.act_url',
                    'url': ("web/content/?model=ir.attachment&id=" + str(attachment.id) + "&download=true&"
                            "filename=" + drawingFilename),
                    'target': 'self',
                }

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        s.close()