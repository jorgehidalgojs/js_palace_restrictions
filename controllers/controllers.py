# -*- coding: utf-8 -*-
# from odoo import http


# class Iniciando(http.Controller):
#     @http.route('/protocolo/protocolo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/protocolo/protocolo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('protocolo.listing', {
#             'root': '/protocolo/protocolo',
#             'objects': http.request.env['protocolo.protocolo'].search([]),
#         })

#     @http.route('/protocolo/protocolo/objects/<model("protocolo.protocolo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('protocolo.object', {
#             'object': obj
#         })
