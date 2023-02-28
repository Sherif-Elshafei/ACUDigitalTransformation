# -*- coding: utf-8 -*-
# from odoo import http


# class Acums(http.Controller):
#     @http.route('/acums/acums', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/acums/acums/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('acums.listing', {
#             'root': '/acums/acums',
#             'objects': http.request.env['acums.acums'].search([]),
#         })

#     @http.route('/acums/acums/objects/<model("acums.acums"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('acums.object', {
#             'object': obj
#         })
