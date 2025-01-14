from odoo import models
from datetime import datetime
from odoo.addons.report_xlsx.report.report_abstract_xlsx import ReportXlsxAbstract
import base64


class PayrollSummaryReportXlsx(ReportXlsxAbstract, models.AbstractModel):
    _name = 'report.payroll_reports.report_payroll_summary_xlsx'
    _description = 'Payroll Summary Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet('Payroll Summary Report')

        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D3D3D3',
            'font_name': 'Times New Roman',
            'font_size': 12})

        total_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'bg_color': '#D3D3D3',
            'num_format': '#,##0.00',
            'font_size': 12})
        footer_format = workbook.add_format(
            {'bold': True,
             'font_size': 12,
             'valign': 'vcenter',
             'font_name': 'Times New Roman'})

        cell_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'num_format': '#,##0.00'
        })
        roll_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })

        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 25)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 25)
        sheet.set_column('I:I', 25)
        sheet.set_column('J:J', 25)
        sheet.set_column('K:K', 25)
        sheet.set_column('L:L', 25)
        sheet.set_column('M:M', 25)
        sheet.set_column('N:N', 25)
        sheet.set_column('O:O', 25)
        sheet.set_column('P:P', 25)
        sheet.set_column('Q:Q', 25)
        sheet.set_column('R:R', 25)
        sheet.set_column('S:S', 25)
        sheet.set_column('T:T', 25)
        sheet.set_column('U:U', 25)
        sheet.set_column('V:V', 25)
        sheet.set_column('W:W', 25)
        sheet.set_column('X:X', 25)
        sheet.set_column('Y:Y', 25)

        company = self.env.company
        company_name = company.name
        company_logo = company.logo

        from_date = data.get('date_from')
        to_date = data.get('date_to')
        if from_date and to_date:
            from_date_date = datetime.strptime(from_date, '%Y-%m-%d')
            only_month = from_date_date.strftime('%B').upper()
            year = from_date_date.year
            for_month = f"For The Month Of {only_month}, {year}"
        else:
            for_month = "Date"

        title_format = workbook.add_format(
            {'bold': True, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 16,
             'font_name': 'Times New Roman'})
        date_format = workbook.add_format(
            {'left': 1, 'right': 1, 'font_size': 16, 'align': 'center', 'valign': 'vcenter', 'bold': True,
             'font_name': 'Times New Roman'})

        sheet.set_row(0, 30)
        sheet.set_row(1, 30)
        sheet.set_row(2, 30)
        sheet.set_column('A:F', 20)

        sheet.merge_range('A1:Y1', company_name, title_format)
        sheet.merge_range('A2:Y2', "Employees Payroll sheet", title_format)

        if company_logo:
            imgdata = base64.b64decode(company_logo)
            image_path = '/tmp/logo.png'
            with open(image_path, 'wb') as f:
                f.write(imgdata)
            # sheet.insert_image('K1', image_path, {'x_scale': 0.6, 'y_scale': 0.6})
        sheet.merge_range('A3:Y3', for_month, date_format)

        heading_rows = 4

        sheet.write('A4', 'NO', header_format)
        sheet.write('B4', 'Employee Name', header_format)
        sheet.write('C4', 'Basic Salary', header_format)
        sheet.write('D4', 'Responsibility Allowance', header_format)
        sheet.write('E4', 'Transport Allowance', header_format)
        sheet.write('F4', 'Over Time Hour 1.25', header_format)
        sheet.write('G4', 'Over Time Hour 1.50', header_format)
        sheet.write('H4', 'Over Time Hour 2.0', header_format)
        sheet.write('I4', 'Over Time Hour 2.5', header_format)
        sheet.write('J4', 'Over Time', header_format)
        sheet.write('K4', 'Commission EVD', header_format)
        sheet.write('L4', 'Commission Telebirr', header_format)
        sheet.write('M4', 'Commission SIM', header_format)
        sheet.write('N4', 'Total Commission', header_format)
        sheet.write('O4', 'Pension 11%', header_format)
        sheet.write('P4', 'Gross Pay', header_format)
        sheet.write('Q4', 'Taxable Income', header_format)
        sheet.write('R4', 'Income Tax', header_format)
        sheet.write('S4', 'Pension 7%', header_format)
        sheet.write('T4', 'Pension 11%', header_format)
        sheet.write('U4', 'Cost Sharing 10%', header_format)
        sheet.write('V4', 'Other Deduction', header_format)
        sheet.write('W4', 'Employee Loan Deduct', header_format)
        sheet.write('X4', 'Total Deduction', header_format)
        sheet.write('Y4', 'Net Salary', header_format)

        row = heading_rows + 1
        domain = []
        if data.get('employee_zones'):
            employees = self.env['hr.employee'].search([('zone_id', 'in', data.get('employee_zones'))])
            domain += [('employee_id', '=', employees.ids)]
        if data.get('date_from'):
            domain.append(('date_from', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date_to', '<=', data.get('date_to')))

        employees_payroll_data = self.env['hr.payslip'].search(domain)

        domain2 = []
        if data.get('employee_zones'):
            employees = self.env['hr.employee'].search([('zone_id', 'in', data.get('employee_zones'))])
            domain2 += [('employee_id', 'in', employees.ids)]
        if data.get('date_from'):
            domain2.append(('date', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain2.append(('date', '<=', data.get('date_to')))
        overtime_data = self.env['hr.employee.overtime'].search(domain2)

        domain3 = []
        if data.get('employee_zones'):
            employees = self.env['hr.employee'].search([('zone_id', 'in', data.get('employee_zones'))])
            domain3 += [('employee_id', 'in', employees.ids)]
        if data.get('date_from'):
            domain3.append(('date', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain3.append(('date', '<=', data.get('date_to')))
        commission_data = self.env['hr.employee.commission'].search(domain3)
        report_data = {}

        for rec in employees_payroll_data:
            unique_data = (rec.employee_id.id, rec.number)
            if unique_data not in report_data:
                report_data[unique_data] = {
                    'employee_name': rec.employee_id.name,
                    'basic_salary': 0,
                    'responsibility_allowance': 0,
                    'transport_allowance': 0,
                    'over_time_125': 0,
                    'over_time_150': 0,
                    'over_time_2': 0,
                    'over_time_25': 0,
                    'over_time': 0,
                    'commission_evd': 0,
                    'commission_teleber': 0,
                    'commission_sim': 0,
                    'total_commission': 0,
                    'gross_pay': 0,
                    'taxable_income': 0,
                    'income_tax': 0,
                    'pension_7': 0,
                    'pension_11': 0,
                    'cost_sharing_10': 0,
                    'other_deduction': 0,
                    'employee_loan_deduct': rec.input_line_ids.amount,
                    'total_deduction': 0,
                    'net_salary': 0
                }

            for emp in rec.line_ids:

                if emp.code == 'BASIC':
                    report_data[unique_data]['basic_salary'] += emp.amount
                elif emp.code == 'RSALL':
                    report_data[unique_data]['responsibility_allowance'] += emp.amount
                elif emp.code == 'Transport':
                    report_data[unique_data]['transport_allowance'] += emp.amount
                elif emp.code == 'OVERTIME':
                    report_data[unique_data]['over_time'] += emp.amount
                elif emp.code == 'COMISSION':
                    report_data[unique_data]['total_commission'] += emp.amount
                elif emp.code == 'GROSS':
                    report_data[unique_data]['gross_pay'] += emp.amount
                elif emp.code == 'TXIN':
                    report_data[unique_data]['taxable_income'] += emp.amount
                elif emp.code == 'INCOME_TAX':
                    report_data[unique_data]['income_tax'] += emp.amount
                elif emp.code == 'Pension 7%':
                    report_data[unique_data]['pension_7'] += emp.amount
                elif emp.code == 'Pension 11%':
                    report_data[unique_data]['pension_11'] += emp.amount
                elif emp.code == 'COST_SHARING_DED':
                    report_data[unique_data]['cost_sharing_10'] += emp.amount
                elif emp.code == 'Meal':
                    report_data[unique_data]['other_deduction'] += emp.amount
                elif emp.code == 'LOAN_DED':
                    report_data[unique_data]['employee_loan_deduct'] += emp.amount
                elif emp.code == 'TLDN':
                    report_data[unique_data]['total_deduction'] += emp.amount
                elif emp.code == 'NET':
                    report_data[unique_data]['net_salary'] += emp.amount

        for commission in commission_data:
            employee_id = commission.employee_id.id
            for each_payroll in employees_payroll_data:
                if employee_id == each_payroll.employee_id.id and each_payroll.date_from <= commission.date <= each_payroll.date_to:
                    unique_employee = (employee_id, each_payroll.number)
        for overtime in overtime_data:
            employee_id = overtime.employee_id.id
            for each_payroll in employees_payroll_data:
                if employee_id == each_payroll.employee_id.id and each_payroll.date_from <= overtime.date <= each_payroll.date_to:
                    unique_employee = (employee_id, each_payroll.number)
                    if overtime.days_selection == 'working_day':
                        report_data[unique_employee]['over_time_125'] += overtime.overtime_duration
                    elif overtime.days_selection == 'holiday':
                        report_data[unique_employee]['over_time_25'] += overtime.overtime_duration
                    elif overtime.days_selection == 'saturday':
                        report_data[unique_employee]['over_time_150'] += overtime.overtime_duration
                    elif overtime.days_selection == 'sunday':
                        report_data[unique_employee]['over_time_2'] += overtime.overtime_duration

        for commission in commission_data:
            employee_id = commission.employee_id.id
            for each_payroll in employees_payroll_data:
                if employee_id == each_payroll.employee_id.id and each_payroll.date_from <= commission.date <= each_payroll.date_to:
                    unique_employee = (employee_id, each_payroll.number)
                    if commission.commission_selection == 'commission_evd':
                        report_data[unique_employee]['commission_evd'] += commission.commission_amount
                    elif commission.commission_selection == 'commission_telebirr':
                        report_data[unique_employee]['commission_teleber'] += commission.commission_amount
                    elif commission.commission_selection == 'commission_sim':
                        report_data[unique_employee]['commission_sim'] += commission.commission_amount

        roll_number = 1
        total_basic_salary = 0
        total_responsibility_all_salary = 0
        total_transport_all_salary = 0
        total_over_time_125_salary = 0
        total_over_time_150_salary = 0
        total_over_time_2_salary = 0
        total_over_time_25_salary = 0
        total_over_time_salary = 0
        total_commission_evd_salary = 0
        total_commission_teleber_salary = 0
        total_commission_sim_salary = 0
        total_total_commission_salary = 0
        total_gross_pay_salary = 0
        total_taxable_income_salary = 0
        total_income_tax_salary = 0
        total_pension_7_salary = 0
        total_pension_11_salary = 0
        total_cost_sharing_10_salary = 0
        total_other_deduction_salary = 0
        total_employee_loan_deduct_salary = 0
        total_total_deduction_salary = 0
        total_net_salary = 0

        for employee_id, item in report_data.items():
            basic_salary = item['basic_salary'] if item['basic_salary'] is not None else ''
            responsibility_allowance = item['responsibility_allowance'] if item[
                                                                               'responsibility_allowance'] is not None else ''
            transport_allowance = item['transport_allowance'] if item['transport_allowance'] is not None else ''
            over_time_125 = item['over_time_125'] if item['over_time_125'] is not None else ''
            over_time_150 = item['over_time_150'] if item['over_time_150'] is not None else ''
            over_time_2 = item['over_time_2'] if item['over_time_2'] is not None else ''
            over_time_25 = item['over_time_25'] if item['over_time_25'] is not None else ''
            over_time = item['over_time'] if item['over_time'] is not None else ''
            commission_evd = item['commission_evd'] if item['commission_evd'] is not None else ''
            commission_teleber = item['commission_teleber'] if item['commission_teleber'] is not None else ''
            commission_sim = item['commission_sim'] if item['commission_sim'] is not None else ''
            total_commission = item['total_commission'] if item['total_commission'] is not None else ''
            pension_11 = item['pension_11'] if item['pension_11'] is not None else ''
            gross_pay = item['gross_pay'] if item['gross_pay'] is not None else ''
            taxable_income = item['taxable_income'] if item['taxable_income'] is not None else ''
            income_tax = item['income_tax'] if item['income_tax'] is not None else ''
            pension_7 = item['pension_7'] if item['pension_7'] is not None else ''
            cost_sharing_10 = item['cost_sharing_10'] if item['cost_sharing_10'] is not None else ''
            other_deduction = item['other_deduction'] if item['other_deduction'] is not None else ''
            employee_loan_deduct = item['employee_loan_deduct'] if item['employee_loan_deduct'] is not None else ''
            total_deduction = item['total_deduction'] if item['total_deduction'] is not None else ''
            net_salary = item['net_salary'] if item['net_salary'] is not None else ''

            basic_salary = float(basic_salary) if isinstance(basic_salary, str) else basic_salary
            responsibility_allowance = float(responsibility_allowance) if isinstance(responsibility_allowance,
                                                                                     str) else responsibility_allowance
            transport_allowance = float(transport_allowance) if isinstance(transport_allowance,
                                                                           str) else transport_allowance
            over_time_125 = float(over_time_125) if isinstance(over_time_125, str) else over_time_125
            over_time_150 = float(over_time_150) if isinstance(over_time_150, str) else over_time_150
            over_time_2 = float(over_time_2) if isinstance(over_time_2, str) else over_time_2
            over_time_25 = float(over_time_25) if isinstance(over_time_25, str) else over_time_25
            over_time = float(over_time) if isinstance(over_time, str) else over_time
            commission_evd = float(commission_evd) if isinstance(commission_evd, str) else commission_evd
            commission_teleber = float(commission_teleber) if isinstance(commission_teleber,
                                                                         str) else commission_teleber
            commission_sim = float(commission_sim) if isinstance(commission_sim, str) else commission_sim
            total_commission = float(total_commission) if isinstance(total_commission, str) else total_commission
            pension_11 = float(pension_11) if isinstance(pension_11, str) else pension_11
            gross_pay = float(gross_pay) if isinstance(gross_pay, str) else gross_pay
            taxable_income = float(taxable_income) if isinstance(taxable_income, str) else taxable_income
            income_tax = float(income_tax) if isinstance(income_tax, str) else income_tax
            pension_7 = float(pension_7) if isinstance(pension_7, str) else pension_7
            cost_sharing_10 = float(cost_sharing_10) if isinstance(cost_sharing_10, str) else cost_sharing_10
            other_deduction = float(other_deduction) if isinstance(other_deduction, str) else other_deduction
            positive_num_other_deduction = abs(other_deduction)
            employee_loan_deduct = float(employee_loan_deduct) if isinstance(employee_loan_deduct,
                                                                             str) else employee_loan_deduct
            total_deduction = float(total_deduction) if isinstance(total_deduction, str) else total_deduction
            net_salary = float(net_salary) if isinstance(net_salary, str) else net_salary

            sheet.write('A' + str(row), roll_number, roll_format)
            sheet.write('B' + str(row), item['employee_name'], cell_format)
            sheet.write('C' + str(row), basic_salary if basic_salary != 0 else '', cell_format)
            sheet.write('D' + str(row), responsibility_allowance if responsibility_allowance != 0 else '', cell_format)
            sheet.write('E' + str(row), transport_allowance if transport_allowance != 0 else '', cell_format)
            sheet.write('F' + str(row), over_time_125 if over_time_125 != 0 else '', cell_format)
            sheet.write('G' + str(row), over_time_150 if over_time_150 != 0 else '', cell_format)
            sheet.write('H' + str(row), over_time_2 if over_time_2 != 0 else '', cell_format)
            sheet.write('I' + str(row), over_time_25 if over_time_25 != 0 else '', cell_format)
            sheet.write('J' + str(row), over_time if over_time != 0 else '', cell_format)
            sheet.write('K' + str(row), commission_evd if commission_evd != 0 else '', cell_format)
            sheet.write('L' + str(row), commission_teleber if commission_teleber != 0 else '', cell_format)
            sheet.write('M' + str(row), commission_sim if commission_sim != 0 else '', cell_format)
            sheet.write('N' + str(row), total_commission if total_commission != 0 else '', cell_format)
            sheet.write('O' + str(row), pension_11 if pension_11 != 0 else '', cell_format)
            sheet.write('P' + str(row), gross_pay if gross_pay != 0 else '', cell_format)
            sheet.write('Q' + str(row), taxable_income if taxable_income != 0 else '', cell_format)
            sheet.write('R' + str(row), income_tax if income_tax != 0 else '', cell_format)
            sheet.write('S' + str(row), pension_7 if pension_7 != 0 else '', cell_format)
            sheet.write('T' + str(row), pension_11 if pension_11 != 0 else '', cell_format)
            sheet.write('U' + str(row), cost_sharing_10 if cost_sharing_10 != 0 else '', cell_format)
            sheet.write('V' + str(row), positive_num_other_deduction if positive_num_other_deduction != 0 else '', cell_format)
            sheet.write('W' + str(row), employee_loan_deduct if employee_loan_deduct != 0 else '', cell_format)
            sheet.write('X' + str(row), total_deduction if total_deduction != 0 else '', cell_format)
            sheet.write('Y' + str(row), net_salary if net_salary != 0 else '', cell_format)

            total_basic_salary += item['basic_salary']
            total_responsibility_all_salary += item['responsibility_allowance']
            total_transport_all_salary += item['transport_allowance']
            total_over_time_125_salary += item['over_time_125']
            total_over_time_150_salary += item['over_time_150']
            total_over_time_2_salary += item['over_time_2']
            total_over_time_25_salary += item['over_time_25']
            total_over_time_salary += item['over_time']
            total_commission_evd_salary += item['commission_evd']
            total_commission_teleber_salary += item['commission_teleber']
            total_commission_sim_salary += item['commission_sim']
            total_total_commission_salary += item['total_commission']
            total_pension_11_salary += item['pension_11']
            total_gross_pay_salary += item['gross_pay']
            total_taxable_income_salary += item['taxable_income']
            total_income_tax_salary += item['income_tax']
            total_pension_7_salary += item['pension_7']
            total_cost_sharing_10_salary += item['cost_sharing_10']
            total_other_deduction_salary += item['other_deduction']
            total_employee_loan_deduct_salary += item['employee_loan_deduct']
            total_total_deduction_salary += item['total_deduction']
            total_net_salary += item['net_salary']
            row += 1
            roll_number += 1

        sheet.write('B' + str(row), 'Total', total_format)
        sheet.write('C' + str(row), total_basic_salary if total_basic_salary != 0 else '', total_format)
        sheet.write('D' + str(row), total_responsibility_all_salary if total_responsibility_all_salary != 0 else '',
                    total_format)
        sheet.write('E' + str(row), total_transport_all_salary if total_transport_all_salary != 0 else '', total_format)
        sheet.write('F' + str(row), total_over_time_125_salary if total_over_time_125_salary != 0 else '', total_format)
        sheet.write('G' + str(row), total_over_time_150_salary if total_over_time_150_salary != 0 else '', total_format)
        sheet.write('H' + str(row), total_over_time_2_salary if total_over_time_2_salary != 0 else '', total_format)
        sheet.write('I' + str(row), total_over_time_25_salary if total_over_time_25_salary != 0 else '', total_format)
        sheet.write('J' + str(row), total_over_time_salary if total_over_time_salary != 0 else '', total_format)
        sheet.write('K' + str(row), total_commission_evd_salary if total_commission_evd_salary != 0 else '',
                    total_format)
        sheet.write('L' + str(row), total_commission_teleber_salary if total_commission_teleber_salary != 0 else '',
                    total_format)
        sheet.write('M' + str(row), total_commission_sim_salary if total_commission_sim_salary != 0 else '',
                    total_format)
        sheet.write('N' + str(row), total_total_commission_salary if total_total_commission_salary != 0 else '',
                    total_format)
        sheet.write('O' + str(row), total_pension_11_salary if total_pension_11_salary != 0 else '', total_format)
        sheet.write('P' + str(row), total_gross_pay_salary if total_gross_pay_salary != 0 else '', total_format)
        sheet.write('Q' + str(row), total_taxable_income_salary if total_taxable_income_salary != 0 else '',
                    total_format)
        sheet.write('R' + str(row), total_income_tax_salary if total_income_tax_salary != 0 else '', total_format)
        sheet.write('S' + str(row), total_pension_7_salary if total_pension_7_salary != 0 else '', total_format)
        sheet.write('T' + str(row),
                    total_pension_11_salary if total_pension_11_salary != 0 else '' if total_pension_11_salary != 0 else '',
                    total_format)
        sheet.write('U' + str(row), total_cost_sharing_10_salary if total_cost_sharing_10_salary != 0 else '',
                    total_format)
        sheet.write('V' + str(row), abs(total_other_deduction_salary) if abs(total_other_deduction_salary) != 0 else '',
                    total_format)
        sheet.write('W' + str(row), total_employee_loan_deduct_salary if total_employee_loan_deduct_salary != 0 else '',
                    total_format)
        sheet.write('X' + str(row), total_total_deduction_salary if total_total_deduction_salary != 0 else '',
                    total_format)
        sheet.write('Y' + str(row), total_net_salary if total_net_salary != 0 else '', total_format)

        row += 2

        sheet.merge_range(row, 1, row, 4, 'Prepared By: _______________', footer_format)
        sheet.merge_range(row, 15, row, 19, 'Checked By :_________________', footer_format)
        sheet.merge_range(row, 21, row, 25, 'Approved by :_________________', footer_format)
