from odoo import models,fields,api

class Form(models.Model):
    _name = "file_upload"

    file_attachment_ids = fields.Many2many('ir.attachment', 'res_id', string='File Attachments')
