from odoo import models
from datetime import datetime
from odoo.addons.report_xlsx.report.report_abstract_xlsx import ReportXlsxAbstract, _logger
import base64


class MerchantSummaryReportXlsx(ReportXlsxAbstract, models.AbstractModel):
    _name = 'report.payroll_reports.report_merchant_summary_xlsx'
    _description = 'Merchant Summary Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet('Merchant Summary Report')

        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D3D3D3',
            'font_size': 12})

        cell_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })
        cell_formatt = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
        })

        sheet.set_column('A:A', 25)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 25)
        sheet.set_column('G:G', 25)

        sheet.write('A1', 'Identifier Type', header_format)
        sheet.write('B1', 'Employee Name', header_format)
        sheet.write('C1', 'Identifier Value', header_format)
        sheet.write('D1', 'Zone', header_format)
        sheet.write('E1', 'Validation KYC value(O)', header_format)
        sheet.write('F1', 'Amount', header_format)
        sheet.write('G1', 'Comment', header_format)

        row = 2
        domain = []
        if data.get('employee_zones'):
            employees = self.env['hr.employee'].search([('zone_id', 'in', data.get('employee_zones'))])
            domain += [('employee_id', 'in', employees.ids)]
        if data.get('date_from'):
            domain.append(('date_from', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date_to', '<=', data.get('date_to')))

        _logger.info('Domain: %s', domain)

        employees_payroll_data = self.env['hr.payslip'].search(domain)

        report_data = {}

        for rec in employees_payroll_data:
            unique_data = (rec.employee_id.id, rec.number)
            if unique_data not in report_data:
                month_name = rec.date_from.strftime('%B')
                comment = f'{month_name} Salary'
                report_data[unique_data] = {
                    'employee_name': rec.employee_id.name,
                    'zone_name': rec.employee_id.zone_id.name,
                    'identifier_type': 'MSISDN',
                    'identifier_value': rec.employee_id.mobile_phone,
                    'net_salary': 0,
                    'comment': comment,
                }

            for emp in rec.line_ids:
                if emp.code == 'NET':
                    report_data[unique_data]['net_salary'] += emp.amount

        for employee_id, item in report_data.items():
            net_salary = item['net_salary'] if item['net_salary'] is not None else ''
            net_salary = float(net_salary) if isinstance(net_salary, str) else net_salary
            sheet.write('A' + str(row), item['identifier_type'], cell_format)
            sheet.write('B' + str(row), item['employee_name'], cell_format)
            sheet.write('C' + str(row), item['identifier_value'], cell_format)
            sheet.write('D' + str(row), item['zone_name'], cell_format)
            sheet.write('E' + str(row), " ", cell_format)
            sheet.write('F' + str(row), net_salary if net_salary != 0 else '', cell_formatt)
            sheet.write('G' + str(row), item['comment'], cell_format)

            row += 1
