# -*- coding: utf-8 -*-
{
    'name': "Employee Hierarchy",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
 
    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts','hr','om_hr_payroll','stock'],

    # always loaded
    'data': [
        'data/zone_data.xml',
        'data/res.country.state.csv',
        'data/res.country.state.city.csv',
        'security/ir.model.access.csv',
        'views/employee_overtime.xml',
        'views/hierarchy_views.xml',
        'data/mail_template.xml',
        'data/reminder_cron.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
