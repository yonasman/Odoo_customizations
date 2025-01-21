{
    'name':'Payment Term Notification',
    'Author': 'Yonas Negese M',
    'depends': [
        'account',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_term_form_inherit.xml',
        'data/cron_payment_term_reminder.xml'
    ],
    'application': True,
    'installable': True
}