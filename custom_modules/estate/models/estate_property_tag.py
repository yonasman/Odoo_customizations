from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name= "estate.property.tag"
    _description= "Estate property tag"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    # sql constraints
    _sql_constraints = [
        ('check_name_uniqueness','UNIQUE(name)','Tag name must be unique')
    ]