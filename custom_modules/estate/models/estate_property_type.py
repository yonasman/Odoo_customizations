from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is an estate property type model"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",  # Target model
        "property_type_id",            # Relational field in the target model
        string='Properties'
    )
    # SQL constraints
    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)', 'Property type must be unique')
    ]
