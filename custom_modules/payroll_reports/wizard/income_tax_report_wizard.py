from odoo import models, fields, api


class PayrollSummaryReportWizard(models.TransientModel):
    _name = 'income.tax.summary.report.wizard'
    _description = 'Income Tax Summary Report Wizard'

    employee_zones = fields.Many2many("business.zone", string="Zones")
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def generate_income_tax_report(self):
        self.ensure_one()

        data = {
            'employee_zones': self.employee_zones.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('payroll_reports.income_tax_summary_xlsx_report').report_action(self, data=data)




