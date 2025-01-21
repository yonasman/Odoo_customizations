from odoo import models, fields

class AccountPaymentTermInherit(models.Model):
    _inherit = 'account.payment.term'

    notify_admin = fields.Boolean(
        string="Notify Admin",
        help="If checked, notify the administrator about this payment term before its due date."
    )