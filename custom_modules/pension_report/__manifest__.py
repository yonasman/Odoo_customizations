{
    'name': 'Pension Report',
    "version": "17.0.1.0.0",
    'summary': 'Pension Reports',
    'depends': [
        'base',
        'hr',
        'om_hr_payroll',
        'employee_hierarchy',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pension_tax_report_wizard.xml',
        'views/pension_tax_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}