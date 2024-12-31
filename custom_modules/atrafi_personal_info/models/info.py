from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError

class ResUsers(models.Model):
    _inherit = "res.users"

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", store=True)
    age = fields.Char(string="Age")
    s_phone = fields.Char(string="Secondary Phone")
    picture = fields.Binary(string="Profile Picture")
    customer_id = fields.Binary(string="Customer ID")
    file_attachment_ids = fields.Many2many(
        'ir.attachment', 'attach_rel', 'doc_id', 'attach_id',
        string="Attachments", help="Upload your documents"
    )

class ResPartner(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", store=True)
    age = fields.Integer(string="Age")
    picture = fields.Binary(string="Profile Picture", attachment=True)
    customer_id = fields.Binary(string="Customer ID")
    s_phone = fields.Char(string="Secondary Phone")

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    attach_rel = fields.Many2many('res.users', 'users_attachment_rel', 'attachment_id', 'document_id', string="Attachment")