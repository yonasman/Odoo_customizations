{
    'name': 'Payroll Reports ',
    "version": "17.0.1.0.0",
    'summary': 'Payroll Reports',
    'author': 'Surafel',
    'depends': [
        'base',
        'hr',
        'om_hr_payroll',
        'employee_hierarchy',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/payroll_report.xml',
        'views/payroll_report_wizard.xml',
        'views/merchant_report_wizard.xml',
        'views/custom_commision_view.xml',
        'views/income_tax_report_wizard.xml',
        'views/pension_tax_report_wizard.xml',
        'views/cost_sharing_report_wizard.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}