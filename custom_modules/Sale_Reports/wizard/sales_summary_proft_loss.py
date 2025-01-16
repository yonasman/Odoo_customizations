from odoo import api, models, fields
from datetime import datetime


class PurchaseReportPurchase(models.TransientModel):
    _name = "sales.summary.report.profit.loss"

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    product_ids = fields.Many2many("product.template", domain=[('type', '=', 'product')])
    customer = fields.Many2many("res.partner")

    def test_one(self, product_ids, date_from, date_to, customer):
        domain = []
        if product_ids:
            domain += [('order_line.product_template_id', 'in', product_ids.ids)]
        if date_from:
            date_from_str = str(date_from)  # Convert date_from to string
            date_from_datetime = datetime.strptime(date_from_str, "%Y-%m-%d")
            domain += [('date_order', '>=', date_from_datetime.strftime("%Y-%m-%d 00:00:00"))]
        if date_to:
            date_to_str = str(date_to)  # Convert date_to to string
            date_to_datetime = datetime.strptime(date_to_str, "%Y-%m-%d")
            domain += [('date_order', '<=', date_to_datetime.strftime("%Y-%m-%d 23:59:59"))]
        if customer:
            domain += [('partner_id', 'in', customer.ids)]

        return self.env['sale.order'].search(domain)

    def generate_report_profit_loss(self):
        return self.env.ref('Sale_Reports.sales_summary_report_report_profit_loss').report_action(self)
