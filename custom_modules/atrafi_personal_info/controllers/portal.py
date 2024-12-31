from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
import base64
from odoo.http import request
import logging
from werkzeug.utils import secure_filename




# Logger for debugging purposes
_logger = logging.getLogger(__name__)


class CustomCustomerPortal(CustomerPortal):
    MANDATORY_BILLING_FIELDS = []  # Make all fields optional
    OPTIONAL_BILLING_FIELDS = [
        "name", "phone", "email", "street", "city", "country_id", "zipcode", "state_id",
        "vat", "company_name", "gender", "age", "picture", "customer_id", "s_phone"
    ]

# # profile picture upload controller
# class CustomFIleUpload(http.Controller):
#     @http.route('/my/account', type='http', auth='public', website=True)
#     def file_upload(self, redirect=None, **kw):
#
#         # get the current user
#         current_user = request.env.user
#         _logger.info(f"Current` user: {current_user}")
#
#         # get the uploaded picture
#         file = kw.get("picture")
#
#         if file:
#             # Secure the file name
#             file_name = secure_filename(file.filename)
#
#             try:
#                 # Read the file in binary mode
#                 file_data = file.read()
#                 if not file_data:
#                     return "File is empty, cannot process it."
#                 print("read")
#                 # Base64 encode the file content
#                 encoded_file = base64.b64encode(file_data)
#                 print("encoded")
#
#                 # Update the user's profile picture (in 'res.users')
#                 # _logger.info(f"Attempting to update profile picture for user {current_user.id}")
#
#                 current_user.write({'image_1920': encoded_file})
#                 print("profile updated")
#                 # Create an attachment in the ir.attachment model
#                 attachment_id = request.env['ir.attachment'].create({
#                     'name': file_name,
#                     'type': 'binary',
#                     'datas': encoded_file,
#                     'res_model': 'res.users',  # The model associated with the attachment (user in this case)
#                     'res_id': current_user.id,  # The user to which this attachment belongs
#                 })
#
#                 current_user.write({
#                     'file_attachment_ids': [(4, attachment_id.id)]  # Link the attachment to the Many2many field
#                 })
#
#                 return request.redirect('/my/home')
#
#             except Exception as e:
#                 # Catch any errors during file processing
#                 return f"Error during file processing: {str(e)}"
#         else:
#             # No file uploaded
#             return "No file uploaded."