{
    'name': 'Sale Reports',
    'version': '1.1',
    'summary': 'Wholesale Reports',
    'sequence': -1000,
    'author': "GraceERP",
    'description': """This module provides comprehensive reports for wholesale operations, including customer  sales""",
    'category': '',
    'website': '',
    'depends': ['base', "sale_management", 'account'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',


        'views/header_footer_template_sales.xml',

        'wizard/sales_summary_report_proft_loss.xml',
        # 'wizard/purchase_report_wizard_view.xml',
        # 'wizard/customer_invoice_wizard_view.xml',
        # 'wizard/vendor_bill_wizard_view.xml',
        # 'wizard/general_report_wizard_view.xml',
        # 'wizard/transaction_report_wizard_view.xml',
        # 'wizard/expense_wizard_view.xml',



        'report/sales_report.xml',

    ],
    'installable': True,
    'application': True,
}
