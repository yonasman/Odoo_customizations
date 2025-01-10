from odoo import models,fields

class CustomReport(models.Model):
    _name = 'pdf.report'
    _description = 'custom report generation model'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')