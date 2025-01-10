import tempfile

from odoo import models
from datetime import datetime
from odoo.addons.report_xlsx.report.report_abstract_xlsx import ReportXlsxAbstract
import base64

from odoo.modules import get_module_resource


class PayrollSummaryReportXlsx(ReportXlsxAbstract, models.AbstractModel):
    _name = 'report.payroll_reports.report_income_tax_summary_xlsx'
    _description = 'Income Tax Summary Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet('Income Tax Summary Report')

        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D3D3D3',
            'font_name': 'Calibri',
            'font_size': 12})

        header_format_new = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11
        })
        header_format_left = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11
        })
        header_format_section = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'right': 1,
            'left': 1,
            'top': 2,
            'bottom': 2,
        })
        header_format_section3 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
        })
        header_format_section33 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'right': 0,
        })

        header_format_black = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'font_color': 'white',
            'valign': 'vcenter',
            'bg_color': '#000000',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True
        })
        header_format_white_top = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',

        })
        header_format_white_toppp = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'bottom',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',

        })

        header_format_white_top_top = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',

        })
        header_format_white_top_roll_no = workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',

        })
        header_format_white_bottom = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'bottom',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',

        })

        header_format_white_last = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',
            'bottom': 0,
            'top': 0,
        })
        header_format_white_sign = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'bg_color': '#ffffff',
            'font_color': 'black',
            'bottom': 1,
            'top': 0,
        })
        header_format_white = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'left': 2,
            'right': 2,
            'bottom': 1,
            'valign': 'vcenter',
            'bg_color': '#ffffff',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True
        })
        header_format_white_2 = workbook.add_format({
            'bold': True,
            'font_color': 'black',
            'border': 1,
            'align': 'center',
            'left': 1,
            'right': 1,
            'bottom': 1,
            'top': 1,
            'valign': 'vcenter',
            'bg_color': '#ffffff',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True
        })
        header_format_white_3 = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'left': 1,
            'right': 1,
            'bottom': 1,
            'top': 1,
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
        })

        total_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0.00',
            'font_size': 12})

        footer_format = workbook.add_format(
            {'bold': True,
             'font_size': 12,
             'valign': 'vcenter',
             'font_name': 'Calibri'})

        cell_format = workbook.add_format({
            'border': 1,
            'align': 'right',
            'font_size': 12,
            'valign': 'vcenter',
        })

        cell_format_end = workbook.add_format({
            'border': 1,
            'align': 'right',
            'font_size': 12,
            'valign': 'vcenter',
        })
        roll_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        roll_format_count = workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'bold': True,
        })

        sheet.set_column('A:A', 25)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 25)
        sheet.set_column('G:G', 30)
        sheet.set_column('H:H', 25)
        sheet.set_column('I:I', 25)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 25)
        sheet.set_column('L:L', 25)

        sheet.write('A1', "Employee TIN", header_format_white_top)
        sheet.write('B1', " Employee Full Name", header_format_white_top)
        sheet.write('C1', ' Start Date', header_format_white_top)
        sheet.write('D1', 'End', header_format_white_top)
        sheet.write('E1', "Basic Salary (If the employee has no basic salary,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('F1',
                    "Transport Allowance (If the employee has no Transport Allowance,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('G1',
                    "Taxable Transport Allowance (If the employee has no Taxable Transport Allowance,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('H1', "Over Time (If the employee has no Over time,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('I1',
                    "Other Taxable Benefit (If the employee has no Other Taxable Benefit,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('J1', "Total Taxable (If the employee has no Total Taxable,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('K1', "Tax withheld (If the employee has no Tax withhled ,Please put 0 - Do not leave it blank)",
                    header_format_white_top)
        sheet.write('L1', "Cost Sharing (If the employee has no Cost Sharing,Please put 0 - Do not leave it blank)",
                    header_format_white_top)

        row = 2

        domain = []
        if data.get('employee_zones'):
            employees = self.env['hr.employee'].search([('zone_id', 'in', data.get('employee_zones'))])
            domain += [('employee_id', 'in', employees.ids)]
        if data.get('date_from'):
            domain.append(('date_from', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date_to', '<=', data.get('date_to')))

        employees_payroll_data = self.env['hr.payslip'].search(domain)

        report_data = {}

        for rec in employees_payroll_data:
            unique_data = (rec.employee_id.id, rec.number)
            if unique_data not in report_data:
                report_data[unique_data] = {
                    'employee_name': rec.employee_id.name,
                    'employee_tin_no': rec.employee_id.employee_tin_no,
                    'employee_start_date': rec.employee_id.employee_start_date,
                    'end_date': 0,
                    'basic_salary': 0,
                    'transport_allowance': 0,
                    'taxable_transport_allowance': 0,
                    'responsibility_allowance': 0,
                    'over_time': 0,
                    'total_commission': 0,
                    'other_taxable_benefit': 0,
                    'taxable_income': 0,
                    'income_tax': 0,
                    'cost_sharing_10': 0,
                    'net_salary': 0
                }

            for emp in rec.line_ids:

                if emp.code == 'BASIC':
                    report_data[unique_data]['basic_salary'] += emp.amount
                elif emp.code == 'Transport':
                    report_data[unique_data]['transport_allowance'] += emp.amount
                elif emp.code == 'OVERTIME':
                    report_data[unique_data]['over_time'] += emp.amount
                elif emp.code == 'COMISSION':
                    report_data[unique_data]['total_commission'] += emp.amount
                elif emp.code == 'TXIN':
                    report_data[unique_data]['taxable_income'] += emp.amount
                elif emp.code == 'INCOME_TAX':
                    report_data[unique_data]['income_tax'] += emp.amount
                elif emp.code == 'COST_SHARING_DED':
                    report_data[unique_data]['cost_sharing_10'] += emp.amount
                elif emp.code == 'NET':
                    report_data[unique_data]['net_salary'] += emp.amount
                elif emp.code == 'RSALL':
                    report_data[unique_data]['responsibility_allowance'] += emp.amount

            report_data[unique_data]['other_taxable_benefit'] = report_data[unique_data]['responsibility_allowance'] + \
                                                                report_data[unique_data]['total_commission']

        for employee_id, item in report_data.items():
            employee_start_date = item.get('employee_start_date')
            if employee_start_date:
                employee_start_date = employee_start_date.strftime('%d/%m/%Y')
            else:
                employee_start_date = ''

            employee_tin_no = item['employee_tin_no'] if item['basic_salary'] is not None else ''
            basic_salary = item['basic_salary'] if item['basic_salary'] is not None else ''
            transport_allowance = item['transport_allowance'] if item['transport_allowance'] is not None else ''
            over_time = item['over_time'] if item['over_time'] is not None else ''
            total_commission = item['total_commission'] if item['total_commission'] is not None else ''
            taxable_income = item['taxable_income'] if item['taxable_income'] is not None else ''
            income_tax = item['income_tax'] if item['income_tax'] is not None else ''
            cost_sharing_10 = item['cost_sharing_10'] if item['cost_sharing_10'] is not None else ''
            net_salary = item['net_salary'] if item['net_salary'] is not None else ''
            other_taxable_benefit = item['other_taxable_benefit'] if item['other_taxable_benefit'] is not None else ''
            end_date = item['end_date'] if item['end_date'] is not None else ''

            basic_salary = float(basic_salary) if isinstance(basic_salary, str) else basic_salary
            transport_allowance = float(transport_allowance) if isinstance(transport_allowance,
                                                                           str) else transport_allowance
            over_time = float(over_time) if isinstance(over_time, str) else over_time
            total_commission = float(total_commission) if isinstance(total_commission, str) else total_commission
            taxable_income = float(taxable_income) if isinstance(taxable_income, str) else taxable_income
            income_tax = float(income_tax) if isinstance(income_tax, str) else income_tax
            cost_sharing_10 = float(cost_sharing_10) if isinstance(cost_sharing_10, str) else cost_sharing_10
            net_salary = float(net_salary) if isinstance(net_salary, str) else net_salary
            end_date = float(end_date) if isinstance(end_date, str) else end_date
            other_taxable_benefit = float(other_taxable_benefit) if isinstance(other_taxable_benefit,
                                                                               str) else total_commission

            sheet.write('A' + str(row), employee_tin_no if employee_tin_no != 0 else '', cell_format)
            sheet.write('B' + str(row), item['employee_name'], cell_format)
            sheet.write('C' + str(row), employee_start_date if employee_start_date != 0 else '0', cell_format)
            sheet.write('D' + str(row), end_date if end_date != 0 else '', cell_format)
            sheet.write('E' + str(row), round(basic_salary, 2) if basic_salary != 0 else '0', cell_format)
            sheet.write('F' + str(row), round(transport_allowance, 2) if transport_allowance != 0 else '0', cell_format)
            sheet.write('G' + str(row), item['taxable_transport_allowance'], cell_format_end)
            sheet.write('H' + str(row), round(over_time, 2) if over_time != 0 else '0', cell_format)
            sheet.write('I' + str(row), round(other_taxable_benefit, 2) if other_taxable_benefit != 0 else '0',
                        cell_format)
            sheet.write('J' + str(row), round(taxable_income, 2) if taxable_income != 0 else '0', cell_format)
            sheet.write('K' + str(row), round(income_tax, 2) if income_tax != 0 else '0', cell_format)
            sheet.write('L' + str(row), round(cost_sharing_10, 2) if cost_sharing_10 != 0 else '0', cell_format)

            row += 1

        workbook.close()
