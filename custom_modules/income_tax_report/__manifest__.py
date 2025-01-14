{
    'name': 'Income Tax Report',
    "version": "17.0.1.0.0",
    'summary': 'Income Tax Reports',
    'depends': [
        'base',
        'hr',
        'om_hr_payroll',
        'employee_hierarchy',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/income_tax_report_wizard.xml',
        'views/income_tax_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}