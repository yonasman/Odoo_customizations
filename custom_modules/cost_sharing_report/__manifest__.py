{
    'name': 'Cost Sharing Report',
    "version": "17.0.1.0.0",
    'summary': 'Cost Sharing Reports',
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
        'views/cost_sharing_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}