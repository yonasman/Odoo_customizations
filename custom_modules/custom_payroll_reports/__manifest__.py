{
    'name': 'Custom Payroll Reports',
    "version": "17.0.1.0.0",
    'summary': 'Custom Payroll Reports',
    'depends': [
        'base',
        'hr',
        'om_hr_payroll',
        'employee_hierarchy',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/cost_sharing_report_wizard.xml',
        'views/income_tax_report_wizard.xml',
        'views/pension_tax_report_wizard.xml',
        'views/payroll_reports.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}