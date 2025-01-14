{
    'name' : 'custom_report_generation',
    'depends': ['base','web'],
    'data': [
    'security/ir.model.access.csv',
    'views/report_menus.xml',
    'views/report_views.xml',
    'views/report_excel_template.xml'
    'report/report_template.xml',
    'report/report_actions.xml',
    ],
}
