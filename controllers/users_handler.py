from odoo import http
from odoo.http import request
import random, string, datetime
import logging
_logger = logging.getLogger(__name__)
def _generate_code(user_id, length=6):
    """
    Generate a random alphanumeric code of the given length and saves that on table
    """
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    user = request.env['easy_user.activation_code'].sudo().create({
            'user_id' : user_id,
            'activation_code' : code
    }) 
    return user.read()[0]['activation_code']

def _regenerate_code(user_id, length=6):
    """
    Generate a random alphanumeric code of the given length and saves that on table
    """
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    user = request.env['easy_user.activation_code'].sudo().search([('user_id', '=', user_id)])
    user.sudo.write({'activation_code': code}) 
    return user.read()[0]['activation_code']

def _send_email(activation_code, email):
    """
    Send an email with the activation code to the specified email address.
    needs to get installed the module Discuss !important
    """
    default_sender_email = request.env['ir.config_parameter'].sudo().get_param('default_sender_email')
    # makes the mail body in mail.mail
    mail_obj = request.env['mail.mail'].sudo().create({
        'subject': 'Your Activation Code',
        'body_html': f"""
            <p>Hello,</p>
            <p>Your activation code is: <strong>{activation_code}</strong></p>
            <p>Please use this code to activate your account.</p>
            <p>Thank you!</p>
        """,
        'email_to': email,
        'email_from': default_sender_email,  
    })
    mail_obj.send()
class EasyUsers(http.Controller):
    @http.route('/api/easy_apps/users/new_user', methods=['POST'], type='json', auth='public', csrf=False, cors='*')
    def create_easy_user(self, **kwargs):
        """
        Endpoint to create users on the group 'easy_apps'.
        """
        try:
            # get the requested data
            email = kwargs.get('email')
            name = kwargs.get('name')
            password = kwargs.get('password')

            if not email or not name or not password:
                return {
                'error': 'Insufficient data',
                'message': 'Fields email, name and password are required'
                }
            #verify if email already exist
            user = request.env['res.users'].sudo().search([('login', '=', email), '|', ('active', '=', True), ('active', '=', False)], limit=1)
            if user:
                return {
                'error': 'Repeated email',
                'message': 'The Email is already registered'
                }
            easy_apps_group_id = request.env['ir.config_parameter'].sudo().get_param('easy_app_group_id') #gets the default groups id
            # Create the user
            new_user = request.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'email': email,
                'password': password,
                'active': False, # default until activate the email
                'groups_id': [(4, request.env.ref('base.group_portal').id), (4, easy_apps_group_id)],  # Add the user at the group ID (easy_apps), the code 4 ensure do not remove any register
            })

            code = _generate_code(new_user.id)
            _send_email(code, email)
            return {
                'success': True,
                'message': 'User created successful',
                'user_id': new_user.id,
            }
        except Exception as e:
            _logger.error(str(e))
            return {
                'error': str(e),
                'message': 'Error creating the user'
            }
    @http.route('/api/easy_apps/users/validate_code', methods=['POST'], type='json', auth='public', csrf=False, cors='*')
    def validate_code(self, **kwargs):
        """
        Endpoint to activate the user when that verify the mail.
        """ 
        try:
            # get the requested data
            email = kwargs.get('email')
            code = kwargs.get('code')
            if not email or not code:
                return {
                'error': 'Insufficient data',
                'message': 'Fields email and code are required'
                }
            user = request.env['res.users'].sudo().search([('login', '=', email), '|', ('active', '=', True), ('active', '=', False)], limit=1)
            if not user:
                return {
                'error': 'Email not exist',
                'message': 'The Email not registered yet'
                }
            user_id = user.id
            if user.active == True:
                return {
                    'error': 'Activated',
                    'message': 'User is already activate'
                }
            code_row = request.env['easy_user.activation_code'].sudo().search([('user_id', '=', user_id)], limit=1)
            now = datetime.datetime.now()
            code_date = str(code_row.write_date) 
            code_time = datetime.datetime.strptime(code_date, "%Y-%m-%d %H:%M:%S.%f")
            two_hours = datetime.timedelta(seconds=7200)
            if (now - code_time) > two_hours:
                return {
                    'error': 'Expired code',
                    'message': 'The code was expired, please try resend that'
                }
            if code_row.activation_code == code:
                user.sudo().write({'active': True})
                return {
                    'success': True,
                    'message': 'User has been successfully activated.'
                }
            else:
                return {
                    'error': 'Invalid activation code',
                    'message': 'The provided activation code is incorrect.'
                }
        except Exception as e:
            _logger.error(str(e))
            return {
                'error': str(e),
                'message': 'Error validating the user'
            }
    @http.route('/api/easy_apps/users/resend_code', methods=['POST'], type='json', auth='public', csrf=False, cors='*')
    def resend_code(self, **kwargs):
        """
        Endpoint to resend code verify the mail, when the code is expired.
        """ 
        try:
            # get the requested data
            email = kwargs.get('email')
            if not email:
                return {
                    'error': 'Insufficient data',
                    'message': 'Fields email are required'
                }
            user = request.env['res.users'].sudo().search([('login', '=', email), '|', ('active', '=', True), ('active', '=', False)], limit=1)
            if not user:
                return {
                'error': 'Email not exist',
                'message': 'The Email not registered yet'
                }
            if user.active == True:
                return {
                    'error': 'Activated',
                    'message': 'User is already activate'
                }
            user_id = user.id
            generated_code = _regenerate_code(user_id)
            _send_email(generated_code, user.login)
            return {
                    'success': True,
                    'message': 'Email sended.'
                }
        except Exception as e:
            _logger.error(str(e))
            return {
                'error': str(e),
                'message': 'Error validating the user'
            }