from odoo import models, fields, api


class FleetDriverSale(models.Model):
    _inherit = 'hr.employee.commission'

    commission_selection = fields.Selection(
        [('commission_evd', 'Commission EVD'), ('commission_telebirr', 'Commission Telebirr'),
         ('commission_sim', 'Commission SIM')],
        string="Commission Selection", required=True)


class EmployeeTinNo(models.Model):
    _inherit = 'hr.employee'

    employee_tin_no = fields.Char(string="Employee TIN No")
    employee_start_date = fields.Date(string="Employee Start Date")


class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'

    employee_tin_no = fields.Char(string="Employee TIN No")
    employee_start_date = fields.Date(string="Employee Start Date")

