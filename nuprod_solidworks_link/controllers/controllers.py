# -*- coding: utf-8 -*-
# from odoo import http


# class NuprodTimeLog(http.Controller):
#     @http.route('/nuprod_time_log/nuprod_time_log', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nuprod_time_log/nuprod_time_log/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nuprod_time_log.listing', {
#             'root': '/nuprod_time_log/nuprod_time_log',
#             'objects': http.request.env['nuprod_time_log.nuprod_time_log'].search([]),
#         })

#     @http.route('/nuprod_time_log/nuprod_time_log/objects/<model("nuprod_time_log.nuprod_time_log"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nuprod_time_log.object', {
#             'object': obj
#         })
