from odoo import api, models, fields


class MerchantReportWizard(models.TransientModel):
    _name = 'merchant.report.wizard'
    _description = 'Merchant Report Wizard'

    employee_zones = fields.Many2many("business.zone", string="Zones")
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)

    def generate_merchant_report(self):
        self.ensure_one()

        data = {
           'employee_zones': self.employee_zones.ids,
           'date_from': self.date_from,
           'date_to': self.date_to
        }
        return self.env.ref('payroll_reports.merchant_xlsx_report').report_action(self, data=data)


