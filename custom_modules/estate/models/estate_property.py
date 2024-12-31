from odoo import models,fields,api
from datetime import date, timedelta
from odoo.exceptions import UserError

from odoo_17.odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate app"
    _order = "id desc"

    name = fields.Char(string='Name',required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=lambda self:(date.today() + timedelta(days=90)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden_area")
    garden_orientation = fields.Selection(string="Garden orientation",selection=[("north","North"),("south","South"),("east","East"),("west","West")])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(selection=[("new","New"),("offer_accepted","Offer Accepted"),("sold","Sold"),("cancelled","Cancelled")],required=True,copy=False,default="new", string="State")
    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    buyer = fields.Many2one('res.partner',string="Buyer", copy=False)
    salesPerson = fields.Char(string="Sales Person", default = lambda self: self.env.user.name)
    property_tag_ids = fields.Many2many('estate.property.tag','property_tag_rel','prop_id','tag_id')
    offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers')
    total_area = fields.Float(string='Total Area(sqm)', compute="_compute_total")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    sequence = fields.Integer()


    # computing total area
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    # compute best price
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            # record.best_price =
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0

    # update garden area and orientation upon updating garden
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    # button actions
    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property can't be sold")
            record.state = 'sold'

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property can't be cancelled")
            record.state = 'cancelled'


    # sql constraints
    _sql_constraints = [
        ('check_selling_price','CHECK(selling_price >= 0)','Selling price must be strictly positive'),
        ('check_offer_price','CHECK(offer_price >= 0)','Offer price must be strictly positive')
    ]

    # python constraints
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.offer_ids.status == "accepted" and record.selling_price < (0.9 * record.expected_price):
                raise UserError("Selling price can't be lower than 90% of the expected price")
