from odoo import models, fields
import io
import base64
from datetime import datetime
import xlsxwriter
from odoo.exceptions import UserError

class ExcelReport(models.Model):
    _name = 'excel.report'
    _description = 'Excel Report Generation'

    # Fields for data collection
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    age = fields.Integer(string='Age')
    department = fields.Char(string='Department')

    def report_excel(self):
        # Collecting data in a structured format
        data = [
            ['First Name', 'Last Name', 'Age', 'Department'],
            [self.first_name, self.last_name, self.age, self.department]
        ]
        # Return the result of generate_excel_report
        return self.generate_excel_report(data)

    def generate_excel_report(self, data):
        # Create an in-memory output stream for the Excel file
        output = io.BytesIO()
        try:
            # Initialize xlsxwriter to create the workbook and sheet
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet('Report')

            # Write data to the sheet
            for row_num, row_data in enumerate(data):
                for col_num, cell_data in enumerate(row_data):
                    sheet.write(row_num, col_num, cell_data)

            workbook.close()
        except Exception as e:
            # Raise an error if the workbook creation fails
            raise UserError(f"Failed to generate Excel report: {str(e)}")

        # Retrieve the binary content of the Excel file
        file_data = output.getvalue()
        output.close()

        # Create an attachment to store the generated file
        attachment = self.env['ir.attachment'].create({
            'name': f'Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(file_data),
            'store_fname': 'report.xlsx',
            'res_model': 'excel.report',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        # Return an action to download the generated report
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }