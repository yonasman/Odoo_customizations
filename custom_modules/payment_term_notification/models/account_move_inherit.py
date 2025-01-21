from odoo import models, fields, api
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model
    def check_payment_terms_due(self):
        """Check for invoices nearing their payment term due date."""
        try:
            # Find all invoices that are posted, not paid, and have a due date
            invoices = self.search([
                ('state', '=', 'posted'),
                ('payment_state', '=', 'not_paid'),
                ('invoice_date_due', '!=', False),
            ])

            # Filter invoices due tomorrow
            tomorrow = fields.Date.today() + timedelta(days=1)
            due_tomorrow = invoices.filtered(lambda inv: inv.invoice_date_due == tomorrow)

            admin_user = self.env.ref('base.user_admin')  # Default administrator user
            if not admin_user:
                return

            for invoice in due_tomorrow:
                # Send email notification
                self.env['mail.mail'].create({
                    'subject': f"Payment Due Reminder: Invoice {invoice.name}",
                    'body_html': f"""
                        <p>Dear Administrator,</p>
                        <p>The payment term for the invoice <b>{invoice.name}</b> is due tomorrow.</p>
                        <p>Kindly ensure necessary actions are taken.</p>
                        <p>Thank you.</p>
                    """,
                    'email_to': admin_user.email,
                }).send(auto_commit=True)

                # Send Discuss inbox notification
                admin_user.partner_id.message_post(
                    body=f"The payment term for the invoice {invoice.name} is due tomorrow. Please take the necessary action. Thank you!",
                    message_type='notification',
                    partner_ids=[admin_user.partner_id.id],
                    subtype_xmlid="mail.mt_note",  # Ensure visibility in Inbox
                )

                _logger.info(f"Notification sent for invoice: {invoice.name}")

        except Exception as e:
            _logger.error(f"Error in check_payment_terms_due: {str(e)}")
