from odoo import http
from odoo.http import request
import base64
from werkzeug.utils import secure_filename


class FileUploadController(http.Controller):
    @http.route(['/form/submit'], type='http', auth='public', website=True)
    def file_upload(self, redirect=None, **kw):
        # Get the current user partner
        current_partner_id = request.env.user.partner_id
        print(f"Current Partner: {current_partner_id}")

        # Get the uploaded file from the form field 'picture'
        file = kw.get('picture')
        print(f"Uploaded File: {file}")

        if file:
            # Secure the file name
            file_name = secure_filename(file.filename)
            print(f"File Name: {file_name}")

            # Create the attachment in the database
            attachment_id = request.env['ir.attachment'].create({
                'name': file_name,
                'type': 'binary',
                'datas': base64.b64encode(file.read()),  # Encode file content to base64
                'res_model': current_partner_id._name,
                'res_id': current_partner_id.id
            })
            print(f"Attachment Created: {attachment_id.id}")

            # Create a new file_upload record and link the attachment to it
            # If a file_upload record doesn't exist, create it
            file_upload = request.env['file_upload'].create({
                'file_attachment_ids': [(4, attachment_id.id)]  # Link the attachment to the Many2many field
            })

            print(f"File Upload Created: {file_upload.id}")
            return "File uploaded and linked successfully!"
        else:
            return "No file uploaded."

    @http.route('/form/view', type='http', auth='public', website=True)
    def upload_image(self):
        return http.request.render('blog_form.website_test')
