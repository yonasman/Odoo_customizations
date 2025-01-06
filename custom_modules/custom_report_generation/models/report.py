from odoo import models,fields,apis

class CustomReport(models.Model):
    _name = 'custom.report'
    _description = 'custom report generation model'

    name = fields.Char(string='name')
    description = fields.Text(string='Description')