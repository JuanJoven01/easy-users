from odoo import http
from odoo.http import request
import random, string
def _generate_code(user_id, length=6):
        """
        Generate a random alphanumeric code of the given length and saves that on table
        """
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        user = request.env['easy_user.activation_code'].sudo().create({
             'user_id' : user_id,
             'activation_code' : code
        }) 
        print('is here **************************************************')
        print(user.read())
        return user.read()[0]['activation_code']

def _verify_code(code, user_id):
        """
        Verify the activation code and activate the user if correct.
        """
        user = request.env['easy_user.activation_code'].sudo().search([('user_id', '=', user_id)], limit=1)
        return True

def _send_email(activation_code):
    print('activation_code ########################')
    print(activation_code)
    return True
class EasyUsers(http.Controller):
    @http.route('/api/easy_apps/users/new_user', methods=['POST'], type='jsonrpc', auth='public')
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
            print('email ##################')
            print(email)
            print('is here 2222222222**************************************************')
            print(user.read())
            if user:
                return {
                'error': 'Repeated email',
                'message': 'The Email is already registered'
                }
            # Create the user
            new_user = request.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'password': password,
                'active': False, # default until activate the email
                'groups_id': [(4, 12)],  # Add the user at the group ID 12 (easy_apps), the code 4 ensure do not remove any register
            })

            code = _generate_code(new_user.id)
            _send_email(code)
            return {
                'success': True,
                'message': 'User created successful',
                'user_id': new_user.id,
            }
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error creating the user'
            }
        oo
