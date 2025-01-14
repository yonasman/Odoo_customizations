import tempfile

from odoo import models
from datetime import datetime
from odoo.addons.report_xlsx.report.report_abstract_xlsx import ReportXlsxAbstract
from odoo.modules import get_module_resource
from odoo.tools.misc import file_path

class PensionTaxSummaryReportXlsx(ReportXlsxAbstract, models.AbstractModel):
    _name = 'report.pension_report.report_pension_tax_summary_xlsx'
    _description = 'Pension Tax Summary Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet('Income Tax Summary Report')

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
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
        })

        header_format_section444 = workbook.add_format({
            'border': 1,
            'bold': True,
            'align': 'right',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
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
            'bold': True,
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
            'bold': True,
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

        header_format_white_bottom_header = workbook.add_format({
            'border': 1,
            'align': 'left',
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
            'num_format': '#,##0.00'
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

        sheet.set_column('A:A', 6)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 20)
        sheet.set_column('L:L', 20)

        company = self.env.company

        from_date = data.get('date_from')
        to_date = data.get('date_to')
        if from_date and to_date:
            from_date_date = datetime.strptime(from_date, '%Y-%m-%d')
            only_month = from_date_date.strftime('%B')
            year = from_date_date.year
            for_month = f"{only_month} {year}"
        else:
            for_month = "Date"

        image_path = get_module_resource('payroll_reports', 'static', 'left.png')

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            tmpfile.write(image_data)
            temp_image_path = tmpfile.name

        image_path2 = get_module_resource('payroll_reports', 'static', 'right.png')

        with open(image_path2, 'rb') as image_file2:
            image_data2 = image_file2.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile2:
            tmpfile2.write(image_data2)
            temp_image_path2 = tmpfile2.name

        sheet.insert_image('A1', temp_image_path, {'x_scale': 1, 'y_scale': 1, 'x_offset': 15, 'y_offset': 10})

        # Sheet setup
        sheet.merge_range('C1:G1', " ", header_format_black)
        sheet.merge_range('C2:G4', "Federal Democratic Republic of Ethiopia Ethiopian \n Revenue and Customs Authority",
                          header_format_black)
        sheet.merge_range('C5:G5', " ", header_format_black)

        # Insert image
        sheet.insert_image('O1', temp_image_path2, {'x_scale': 1.2, 'y_scale': 1, 'x_offset': 15, 'y_offset': 10})
        sheet.merge_range('O1:P5', " ", header_format_white)

        # Title
        sheet.merge_range('H2:N3', "PENSION CONTRIBUTION DECLARATION FORM - PRIVATE", header_format_white_toppp)
        sheet.merge_range('H4:N4', "(PENSION CONTRIBUTION pro. No.175/2003)", header_format_new)

        # Section 1
        sheet.merge_range('A6:P6', "Section 1-Taxpayer Information", header_format_section)
        sheet.merge_range('A7:E7', "1. Taxpayer's Name", header_format_left)
        sheet.merge_range('F7:J7', "3. Taxpayer Identification Number", header_format_left)
        sheet.merge_range('K7:N7', '4. Tax Account Number', header_format_new)
        sheet.write('O7', "8. Period", header_format_left)
        sheet.write('P7', "", header_format_left)

        # Removed conflicting merge range 'D7:G7'
        sheet.merge_range('D8:E8', " ", header_format_white_3)  # Adjusted range here

        # Taxpayer information
        sheet.merge_range('A8:C8', 'TELEPORT TECHNOLOGIES PLC', header_format_left)  # Adjusted range
        sheet.merge_range('F8:H8', '0051852115', header_format_left)  # Adjusted range here
        sheet.merge_range('I8:K8', 'Bulehora', header_format_left)  # Adjusted range here
        sheet.merge_range('L8:N8', for_month, header_format_new)  # Adjusted range here

        # Additional information
        sheet.write('A9', '2. Region', header_format_left)
        sheet.merge_range('C9:E9', '2b. Zone/K-Ketema', header_format_left)
        sheet.merge_range('G9:M9', '5. Tax Center', header_format_left)
        sheet.merge_range('N9:P9', 'Document Number', header_format_new)

        # Region and address details
        sheet.merge_range('A10:B10', '14', header_format_new)
        sheet.merge_range('C10:E10', 'KIRKOS', header_format_new)
        sheet.merge_range('G10:M10', 'Addis Abeba', header_format_new)

        sheet.merge_range('A11:B11', '2c. Woreda', header_format_new)
        sheet.merge_range('C11:D11', '2d. Kebele/Farmers Association', header_format_left)
        sheet.merge_range('E11:G11', '2e. House Number', header_format_left)
        sheet.merge_range('H11:J11', '6. Telephone Number', header_format_new)
        sheet.merge_range('K11:M11', '7. Fax Number', header_format_new)

        sheet.merge_range('A12:B12', '8', header_format_new)
        sheet.merge_range('E12:G12', 'NEW/505', header_format_new)
        sheet.merge_range('H12:J12', '0115-150780', header_format_new)

        sheet.merge_range('N10:P12', '(official use only)', header_format_white_2)

        # Section 2
        sheet.merge_range('A13:P13', 'Section 2-Declaration detail information', header_format_section)
        heading_rows = 15

        # Declaration detail table headings
        sheet.merge_range('A14:A15', 'S.N', header_format_white_top)
        sheet.merge_range('B14:B15', "Employee's TIN No.", header_format_white_top)
        sheet.merge_range('C14:E15', 'Employee Full Name', header_format_white_top)
        sheet.merge_range('F14:F15', 'Date of Employment', header_format_new)
        sheet.merge_range('G14:G15', 'Basic Salary', header_format_new)
        sheet.merge_range('H14:I15', 'Pension contribution by employee(7%)', header_format_new)
        sheet.merge_range('J14:L15', 'Pension contribution by employer(11%)', header_format_new)
        sheet.merge_range('M14:N15', 'Total Contribution', header_format_new)
        sheet.merge_range('O14:P15', 'Signature', header_format_new)

        row = heading_rows + 1
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
                    'employee_start_date': rec.employee_id.employee_start_date,
                    'employee_tin_no': rec.employee_id.employee_tin_no,
                    'basic_salary': 0,
                    'pension_7': 0,
                    'pension_11': 0,
                    'total_commission': 0,
                }

            for emp in rec.line_ids:

                if emp.code == 'BASIC':
                    report_data[unique_data]['basic_salary'] += emp.amount
                elif emp.code == 'Pension 7%':
                    report_data[unique_data]['pension_7'] += emp.amount
                elif emp.code == 'Pension 11%':
                    report_data[unique_data]['pension_11'] += emp.amount

            report_data[unique_data]['total_commission'] = report_data[unique_data]['pension_7'] + \
                                                           report_data[unique_data]['pension_11']

        roll_number = 1
        total_basic_salary = 0
        total_pension_7_salary = 0
        total_pension_11_salary = 0
        total_total_commission_salary = 0

        for employee_id, item in report_data.items():
            employee_tin_no = item['employee_tin_no'] if item['employee_tin_no'] is not None else ''
            employee_start_date = item.get('employee_start_date')
            if employee_start_date:
                employee_start_date = employee_start_date.strftime('%d/%m/%Y')
            else:
                employee_start_date = ''
            basic_salary = item['basic_salary'] if item['basic_salary'] is not None else ''
            pension_11 = item['pension_11'] if item['pension_11'] is not None else ''
            pension_7 = item['pension_7'] if item['pension_7'] is not None else ''
            total_commission = item['total_commission'] if item['total_commission'] is not None else ''

            basic_salary = float(basic_salary) if isinstance(basic_salary, str) else basic_salary
            pension_11 = float(pension_11) if isinstance(pension_11, str) else pension_11
            total_commission = float(total_commission) if isinstance(total_commission, str) else total_commission
            pension_7 = float(pension_7) if isinstance(pension_7, str) else pension_7

            sheet.write('A' + str(row), roll_number, roll_format)
            sheet.write('B' + str(row), employee_tin_no if employee_tin_no != 0 else '', cell_format)
            sheet.merge_range(f'C{row}:E{row}', item['employee_name'], cell_format)
            sheet.write('F' + str(row), employee_start_date if employee_start_date != 0 else '', cell_format)
            sheet.write('G' + str(row), basic_salary if basic_salary != 0 else '', cell_format)
            sheet.merge_range(f'H{row}:I{row}', pension_7 if pension_7 != 0 else '', cell_format)
            sheet.merge_range(f'J{row}:L{row}', pension_11 if pension_11 != 0 else '', cell_format)
            sheet.merge_range(f'M{row}:N{row}', total_commission if total_commission != 0 else '', cell_format)
            sheet.merge_range(f'O{row}:P{row}', " ", cell_format)

            total_basic_salary += item['basic_salary']
            total_pension_7_salary += item['pension_7']
            total_pension_11_salary += item['pension_11']
            total_total_commission_salary = total_pension_11_salary + total_pension_7_salary
            row += 1
            roll_number += 1

        sheet.merge_range(f'C{row}:F{row}', "TOTAL", total_format)
        sheet.write('G' + str(row), total_basic_salary if total_basic_salary != 0 else '', total_format)
        sheet.merge_range(f'H{row}:I{row}', total_pension_7_salary if total_pension_7_salary != 0 else '', total_format)
        sheet.merge_range(f'J{row}:L{row}', total_pension_11_salary if total_pension_11_salary != 0 else '',
                          total_format)
        sheet.merge_range(f'M{row}:N{row}', total_total_commission_salary if total_total_commission_salary != 0 else '',
                          total_format)
        sheet.merge_range(f'O{row}:P{row}', " ", total_format)

        start_row = row + 0
        start_col = 0

        sheet.merge_range(start_row, start_col, start_row, start_col + 3, "Section 3 - Summarized amount for the Month",
                          header_format_section33)
        sheet.write(start_row + 1, 0, "10", header_format_white_top_roll_no)
        sheet.write(start_row + 2, 0, "20", header_format_white_top_roll_no)
        sheet.write(start_row + 3, 0, "30", header_format_white_top_roll_no)
        sheet.write(start_row + 4, 0, "40", header_format_white_top_roll_no)
        sheet.write(start_row + 5, 0, "50", header_format_white_top_roll_no)
        sheet.merge_range(start_row + 1, start_col + 1, start_row + 1, start_col + 2, "Total No of Employees",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 2, start_col + 1, start_row + 2, start_col + 2, "Total Salary",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 3, start_col + 1, start_row + 3, start_col + 2,
                          "Total pension contribution by employee 0.07%", header_format_white_top_top)
        sheet.merge_range(start_row + 4, start_col + 1, start_row + 4, start_col + 2,
                          "Total pension contribution by employer 11%", header_format_white_top_top)
        sheet.merge_range(start_row + 5, start_col + 1, start_row + 5, start_col + 2, "Total pension contribution ",
                          header_format_white_top_top)

        sheet.write(start_row + 1, 3, roll_number - 1, roll_format_count)
        sheet.write(start_row + 2, 3, total_basic_salary, total_format)
        sheet.write(start_row + 3, 3, total_pension_7_salary, total_format)
        sheet.write(start_row + 4, 3, total_pension_11_salary, total_format)
        sheet.write(start_row + 5, 3, total_total_commission_salary, total_format)

        sheet.merge_range(start_row, start_col + 5, start_row, start_col + 9,
                          "Section 4 - List Of Employees Who Left The Company this Month",
                          header_format_section33)

        sheet.write(start_row + 1, start_col + 5, "SN", header_format_white_top_top)
        sheet.merge_range(start_row + 1, start_col + 6, start_row + 1, start_col + 7, "Employees TIN No.",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 1, start_col + 8, start_row + 1, start_col + 9, "Employee Full Name",
                          header_format_white_top_top)

        sheet.write(start_row + 2, start_col + 5, "1", header_format_white_bottom)
        sheet.write(start_row + 3, start_col + 5, "", header_format_white_bottom)
        sheet.write(start_row + 4, start_col + 5, "", header_format_white_bottom)
        sheet.write(start_row + 5, start_col + 5, "", header_format_white_bottom)

        sheet.merge_range(start_row + 2, start_col + 6, start_row + 2, start_col + 7, "",
                          header_format_white_bottom)
        sheet.merge_range(start_row + 3, start_col + 6, start_row + 3, start_col + 7, "",
                          header_format_white_bottom)
        sheet.merge_range(start_row + 4, start_col + 6, start_row + 4, start_col + 7, "",
                          header_format_white_bottom)
        sheet.merge_range(start_row + 5, start_col + 6, start_row + 5, start_col + 7, "",
                          header_format_white_bottom)

        sheet.merge_range(start_row + 2, start_col + 8, start_row + 2, start_col + 9, "",
                          header_format_white_bottom)
        sheet.merge_range(start_row + 3, start_col + 8, start_row + 3, start_col + 9, "",
                          header_format_white_bottom)
        sheet.merge_range(start_row + 4, start_col + 8, start_row + 4, start_col + 9, "",
                          header_format_white_bottom)
        sheet.merge_range(start_row + 5, start_col + 8, start_row + 5, start_col + 9, "",
                          header_format_white_bottom)

        sheet.merge_range(start_row, start_col + 11, start_row, start_col + 15,
                          "For Office Use Only",
                          header_format_section444)

        sheet.merge_range(start_row + 1, start_col + 11, start_row + 1, start_col + 13, "Payment Date",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 2, start_col + 11, start_row + 2, start_col + 13, "Receipt No.",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 3, start_col + 11, start_row + 3, start_col + 13, "Amount",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 4, start_col + 11, start_row + 4, start_col + 13, "Cheque No.",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 5, start_col + 11, start_row + 5, start_col + 13, "Cashier's Name",
                          header_format_white_top_top)

        sheet.merge_range(start_row + 1, start_col + 14, start_row + 1, start_col + 15, "",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 2, start_col + 14, start_row + 2, start_col + 15, "",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 3, start_col + 14, start_row + 3, start_col + 15, "",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 4, start_col + 14, start_row + 4, start_col + 15, "",
                          header_format_white_top_top)
        sheet.merge_range(start_row + 5, start_col + 14, start_row + 5, start_col + 15, "",
                          header_format_white_top_top)

        section5_start_row = start_row + 6
        section5_col = 0

        sheet.merge_range(section5_start_row, section5_col, section5_start_row, section5_col + 15, "Section 5",
                          header_format_section3)
        sheet.merge_range(section5_start_row + 1, section5_col, section5_start_row + 3, section5_col + 3, " ",
                          header_format_white_top)
        sheet.merge_range(section5_start_row + 1, section5_col + 4, section5_start_row + 1, section5_col + 8,
                          "Tax Payer's authorized Signatory:",
                          header_format_white_bottom_header)
        sheet.merge_range(section5_start_row + 2, section5_col + 4, section5_start_row + 2, section5_col + 8,
                          "Name:",
                          header_format_white_bottom_header)
        sheet.merge_range(section5_start_row + 3, section5_col + 4, section5_start_row + 3, section5_col + 6,
                          "Signature:",
                          header_format_white_bottom_header)
        sheet.merge_range(section5_start_row + 3, section5_col + 7, section5_start_row + 3, section5_col + 8,
                          "Date:",
                          header_format_white_bottom_header)

        sheet.merge_range(section5_start_row + 1, section5_col + 9, section5_start_row + 3, section5_col + 11, "Seal",
                          header_format_white_bottom)
        sheet.merge_range(section5_start_row + 1, section5_col + 12, section5_start_row + 1, section5_col + 15, " ",
                          header_format_white_last)
        sheet.merge_range(section5_start_row + 2, section5_col + 12, section5_start_row + 2, section5_col + 15, "Date:",
                          header_format_white_last)
        sheet.merge_range(section5_start_row + 3, section5_col + 12, section5_start_row + 3, section5_col + 15,
                          "Signature:", header_format_white_sign)

        # workbook.close()
