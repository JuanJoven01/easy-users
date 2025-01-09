# -*- coding: utf-8 -*-
# from odoo import http


# class EasyUsers(http.Controller):
#     @http.route('/easy_users/easy_users', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/easy_users/easy_users/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('easy_users.listing', {
#             'root': '/easy_users/easy_users',
#             'objects': http.request.env['easy_users.easy_users'].search([]),
#         })

#     @http.route('/easy_users/easy_users/objects/<model("easy_users.easy_users"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('easy_users.object', {
#             'object': obj
#         })

