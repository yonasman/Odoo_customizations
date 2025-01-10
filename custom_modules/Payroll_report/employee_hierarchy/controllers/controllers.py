# -*- coding: utf-8 -*-
# from odoo import http


# class BusinessFlow(http.Controller):
#     @http.route('/business_flow/business_flow', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/business_flow/business_flow/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('business_flow.listing', {
#             'root': '/business_flow/business_flow',
#             'objects': http.request.env['business_flow.business_flow'].search([]),
#         })

#     @http.route('/business_flow/business_flow/objects/<model("business_flow.business_flow"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('business_flow.object', {
#             'object': obj
#         })
