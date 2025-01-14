from odoo import models, fields, api


class CostSharingSummaryReportWizard(models.TransientModel):
    _name = 'cost.sharing.summary.report.wizard'
    _description = 'Cost Sharing Summary Report Wizard'

    employee_zones = fields.Many2many("business.zone", string="Zones")
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def generate_cost_sharing_report(self):
        self.ensure_one()

        data = {
            'employee_zones': self.employee_zones.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('cost_sharing_report.cost_sharing_summary_xlsx_report').report_action(self, data=data)