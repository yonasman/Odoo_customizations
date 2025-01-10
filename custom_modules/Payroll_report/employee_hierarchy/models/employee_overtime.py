from odoo import models, fields,_, api
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import date


class HrEmployeeOvertime(models.Model):
    _name = "hr.employee.overtime"
    _description = "Employee's Overtime Details"

    name              = fields.Char(string="Overtime Reason")
    employee_id       = fields.Many2one("hr.employee", string='Employee',required=True)
    overtime_duration = fields.Float(string="Overtime", required=True)
    overtime_amount   = fields.Float(string="Amount")
    date              = fields.Date(string="Date")
    payslip_id  = fields.Many2one('hr.payslip',string="Payslip")
    days_selection = fields.Selection([('working_day','Working Days'),('holiday','Holiday'),('saturday','Saturday'),('sunday','Sunday')], string="Day Selection")
        
class HrEmployeeBouns(models.Model):
    _name = "hr.employee.bonus"
    _description = "Employee's Bouns Details"

    name         = fields.Char(string="Reason")
    employee_id  = fields.Many2one(comodel_name="hr.employee",string='Employee',required=True)
    bouns_amount = fields.Float(string="Amount",required=True)
    date         = fields.Date(string="Date")
    payslip_id  = fields.Many2one('hr.payslip',string="Payslip")

class HrEmployeeCommission(models.Model):
    _name = "hr.employee.commission"
    _description = "Employee's Commission Details"

    name         = fields.Char(string="Reason")
    employee_id  = fields.Many2one(comodel_name="hr.employee",string='Employee',required=True)
    commission_amount = fields.Float(string="Amount",required=True)
    date         = fields.Date(string="Date")
    payslip_id  = fields.Many2one('hr.payslip',string="Payslip")

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    _description = 'Employee Public'
    
    branch_id = fields.Many2one('res.branch',string="Branch")
    zone_id = fields.Many2one('business.zone',string="Zone/Region")
    cost_sharing = fields.Boolean('Is Cost Sharing')

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Employee Contract'


    overtime_ids = fields.One2many('hr.employee.overtime','payslip_id',string="Overtime",compute='fetch_employee_bouns_overtime')
    bouns_ids = fields.One2many('hr.employee.bonus','payslip_id',string="Bouns",compute='fetch_employee_bouns_overtime')
    commission_ids = fields.One2many('hr.employee.commission','payslip_id',string="Commission",compute='fetch_employee_bouns_overtime')

    @api.depends('employee_id','date_from','date_to')
    def fetch_employee_bouns_overtime(self):
        overtime_obj = self.env['hr.employee.overtime']
        bouns_obj = self.env['hr.employee.bonus']
        commission_obj = self.env['hr.employee.commission']
        for rec in self:
            if rec.employee_id.contract_id:
                rec.contract_id = rec.employee_id.contract_id
            else:
                rec.contract_id = False
            if rec.employee_id:
                bouns_ids = bouns_obj.search([('employee_id','=',rec.employee_id.id),('date','<=',rec.date_to),('date','>=',rec.date_from)])
                overtime_ids = overtime_obj.search([('employee_id','=',rec.employee_id.id),('date','<=',rec.date_to),('date','>=',rec.date_from)])
                commission_ids = commission_obj.search([('employee_id','=',rec.employee_id.id),('date','<=',rec.date_to),('date','>=',rec.date_from)])
                if bouns_ids:
                    rec.bouns_ids = bouns_ids.ids
                else:
                    rec.bouns_ids = False
                if overtime_ids:
                    rec.overtime_ids = overtime_ids.ids
                else:
                    rec.overtime_ids = False
                if commission_ids:
                    rec.commission_ids = commission_ids.ids
                else:
                    rec.commission_ids = False


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"

    cost_sharing = fields.Boolean('Is Cost Sharing')



        
