from odoo import models, fields, api


class PensionTaxSummaryReportWizard(models.TransientModel):
    _name = 'pension.tax.summary.report.wizard'
    _description = 'Income Tax Summary Report Wizard'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def generate_pension_tax_report(self):
        self.ensure_one()

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('custom_payroll_reports.pension_tax_summary_xlsx_report').report_action(self, data=data)