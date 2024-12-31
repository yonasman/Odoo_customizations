from datetime import timedelta,date
from odoo import models, fields, api

from odoo_17.odoo.exceptions import ValidationError, UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"


    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    creation_date = fields.Date(string="Creation Date", readonly=True, default=date.today())
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_deadline_date',
        inverse="_inverse_deadline_date",
        store=True,
    )

    # Compute the deadline date
    @api.depends('creation_date', 'validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.creation_date:
                record.date_deadline = record.creation_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    # Inverse the validity upon editing the deadline
    # Inverse function for deadline
    def _inverse_deadline_date(self):
        for record in self:
            if record.date_deadline and record.creation_date:
                delta = record.date_deadline - record.creation_date
                record.validity = delta.days
            else:
                record.validity = 0
    # button actions
    def action_confirm(self):
        for record in self:
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'


    def action_refuse(self):
        for record in self:
            record.property_id.buyer = ''
            record.property_id.selling_price = 0
            record.status = 'refused'

    # sql constraints
    _sql_constraints = [
        ('checK_price','CHECK(price >= 0)','Price must be strictly positive')
    ]
