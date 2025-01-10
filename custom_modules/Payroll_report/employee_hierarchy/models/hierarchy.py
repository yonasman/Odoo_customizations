# -*- coding: utf-8 -*-

from odoo import models, fields,_, api
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import date


class ContractType(models.Model):
    _inherit = 'hr.contract.type'
    _description = 'Contract Type'

    # probation_period = fields.Integer(string='Probation Period Days')
    # reminder_cron_job = fields.Integer(string='Remind before')
    # renewal_months = fields.Integer(string='Renewal Months')

class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'


    contract_state = fields.Selection([('',''),("renewable", "Renewable"),("hold", "Hold"),("Close",'Closed')],string='Contract Status')
    operation_manager_id = fields.Many2one('res.users',string="Operation Manager",related='employee_id.zone_id.operation_manager_id.user_id')
    # , 'type_id.probation_period', 'type_id.reminder_cron_job'
    @api.depends('date_start','date_end')
    def compute_expiration_days(self):
        if self.date_start:
            self.date_end = self.date_start + timedelta(days=self.type_id.probation_period) 
        if self.date_end:
            self.contract_expired_after = (self.date_end-self.date_start).days
        if self.date_end and self.type_id.renewal_months<1:
            self.contract_expired_reminder_date = self.date_end - timedelta(days=self.type_id.reminder_cron_job)
        if self.date_end and self.type_id.renewal_months>1:
            self.contract_expired_reminder_date = self.date_end - timedelta(days=self.type_id.renewal_months)




        
    contract_expired_after = fields.Char(compute='compute_expiration_days')
    contract_expired_reminder_date = fields.Date('Contract Expired Reminder Date')

    def submission_for_update_contract(self):
        self.contract_state = 'renewable'

    

    def update_contract(self):
        self.state = 'open'
        self.contract_state = ''
        self.date_end = date.today() + timedelta(days=self.type_id.probation_period)
        self.date_start = date.today()
        self.contract_expired_after = (self.date_end-self.date_start).days


    def remainder_for_new_contract(self):
        contracts = self.env['hr.contract'].search([('state','in',['open'])])
        for rec in contracts:
            employees = self.env['hr.employee'].search([('id','=',rec.hr_responsible_id.employee_id.id)])
            zones = self.env['business.zone'].search([('id','=',rec.employee_id.zone_id.id)])

            if employees:
                if rec.contract_expired_reminder_date and (date.today()>=rec.contract_expired_reminder_date):
                    rec.contract_state = 'hold'
                    
                    message = ("The contract of %s will be expired soon kindly update the contract")  % (rec.employee_id.name)
                    res = rec.sudo().message_post(
                                       body=(message),
                                       message_type='comment',
                                       subtype_xmlid='mail.mt_comment',
                                           )
                    res = employees.sudo().message_post(
                                       body=(message),
                                       message_type='comment',
                                       subtype_xmlid='mail.mt_comment',
                                           )
                    for zone in zones:
                        if zone.operation_manager_id:
                            zone.operation_manager_id.sudo().message_post(
                                       body=(message),
                                       message_type='comment',
                                       subtype_xmlid='mail.mt_comment',)

                if rec.date_end:
                    if (date.today() > rec.date_end) and rec.state=='open':
                        rec.state = 'close'
                        message = ("The contract of %s has been expired")  % (rec.employee_id.name)
                        res = rec.sudo().message_post(
                                           body=(message),
                                           message_type='comment',
                                           subtype_xmlid='mail.mt_comment',
                                               )
                        res = employees.sudo().message_post(
                                       body=(message),
                                       message_type='comment',
                                       subtype_xmlid='mail.mt_comment',
                                           )
                        for zone in zones:
                            if zone.operation_manager_id:
                                zone.operation_manager_id.sudo().message_post(
                                           body=(message),
                                           message_type='comment',
                                           subtype_xmlid='mail.mt_comment',)


    



 
class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    department_ids = fields.One2many('hr.department','employee_id',string="Departments")
    branch_id = fields.Many2one('res.branch',string="Branch")
    branch_ids = fields.Many2many('res.branch',string="Branches")
    zone_id = fields.Many2one('business.zone',string="Zone/Region")

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    employee_id = fields.Many2one('hr.employee')
    
    
class ResCountryState(models.Model):
    _inherit = 'res.country.state'
    _description = "states"

    city_ids = fields.One2many('res.country.state.city', 'state_id', string="Cities")

class BusinessAreas(models.Model):
    _name = 'res.country.state.city'
    _description = "Cities"

    name = fields.Char(string='Name',required=True)
    code = fields.Char(string='Code',required=True)
    country_id = fields.Many2one('res.country',string="Country",  default=lambda self: self.env.company.country_id)
    state_id = fields.Many2one('res.country.state',string="State")
    branch_ids = fields.One2many('res.branch','city',string="Branches")
    zone_id = fields.Many2one('business.zone',string="Zone/Region")
    
    

class BusinessZones(models.Model):
    _name = 'business.zone'
    _description = "Business Zones"

    name = fields.Char(string='Name',required=True)
    code = fields.Char(string='Code',required=True)
    city_ids = fields.One2many('res.country.state.city','zone_id',string="Cities")
    country_id = fields.Many2one('res.country',string="Country",  default=lambda self: self.env.company.country_id)
    manager_id = fields.Many2one('hr.employee',string="Manager")
    operation_manager_id = fields.Many2one('hr.employee',string="Regional Operation Manager")

    def action_total_employee_count(self):
        current_employees_ids = self.env['hr.employee'].search([('zone_id','=',self.id)])
        self.employee_count = len(current_employees_ids)

    employee_count = fields.Integer('Employees', compute='action_total_employee_count')


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s (%s)' % (rec.code,rec.name)))
        return result

    @api.constrains('code')
    def _check_name(self):
        zone_rec = self.env['business.zone'].search(
            [('code', '=', self.code),('id', '!=', self.id)])
        if zone_rec:
            raise ValidationError(_('Exists ! Already a Zone exists with this code'))


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = "company"

    branch_ids = fields.One2many('res.branch', 'company_id', string="Cities")
    

class StockWarehouse(models.Model):
    _inherit='stock.warehouse'

    branch_id = fields.Many2one('res.partner', string='Branch')
    res_branch_id = fields.Many2one('res.branch',string='Related Branch')
    zone_id = fields.Many2one(related="res_branch_id.zone_id", string='Zone', store=True)
 
    

class Branchs(models.Model):
    _name = 'res.branch'
    _description = "Branch"

    name = fields.Char(string='Branch Name',required=True)
    code = fields.Char(string='Branch Code',required=True)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    state_id = fields.Many2one('res.country.state',string="State")
    country_id = fields.Many2one('res.country',string="Country")
    zip_code = fields.Char(string="Pincode")
    mobile_no = fields.Char('Mobile')
    phone = fields.Char('Phone')
    branch_type_sel = fields.Selection([('branch','Branch'),('outlet','Outlet')],string="Branch Selection")
    is_main = fields.Boolean(default='True',string="Is Main Branch")    
    branch_type = fields.Selection(string='Branch Type',  selection=[('main', 'Is Main'), ('sub-branch', 'Child Branch')], default='sub-branch')
    country_id = fields.Many2one('res.country',string="Country",  default=lambda self: self.env.company.country_id)
    state_id = fields.Many2one('res.country.state',string="State")
    zone_id = fields.Many2one('business.zone',string="Zone/Region")
    city = fields.Many2one('res.country.state.city',string="City")
    manager_id = fields.Many2one('hr.employee',string="Manager")
    parent_id = fields.Many2one('res.branch',string="Main Branch")
    company_id = fields.Many2one('res.company',string="Company",  default=lambda self: self.env.company)
    operation_manager_id = fields.Many2one('hr.employee',string="Regional Operation Manager")


    def action_total_employee_count(self):
        current_employees_ids = self.env['hr.employee'].search([('branch_id','=',self.id)])
        self.employee_count = len(current_employees_ids)

    employee_count = fields.Integer('Employees', compute='action_total_employee_count')

    @api.constrains('code')
    def _check_name(self):
        zone_rec = self.env['res.branch'].search(
            [('code', '=', self.code),('id', '!=', self.id)])
        if zone_rec:
            raise ValidationError(_('Exists ! Already a Branch exists with this code'))

    @api.model
    def create(self, vals):
        res = super(Branchs, self).create(vals)
        values = {
             'branch_id':res.id,
             'name':res.company_id.name + ' - ' + res.code,
             'code':res.code,
             'company_id':res.company_id.id
                 }
        warehouse_id = self.env['stock.warehouse'].create(values)
        return res



    
